# Copyright (c) 2022 Paul Irofti <paul@irofti.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import hashlib
import logging
import multiprocessing
import os
import pickle
import time
from collections.abc import Iterable
from pathlib import Path

import numpy as np
from sklearn.base import clone
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import ParameterGrid
from tensorflow.keras.models import load_model


class GridSearch:
    """Grid Search routine.

    Grid search expects an estimator and a set of multiple parameters values
    for each possible parameter of the estimator on which to `fit` the provided
    dataset.

    At the end, the resulting estimators, together with the parameters
    and results, are stored in the `estimators_` attribute. These are also
    stored on disk as separated files inside the `datadir` directory. The naming
    convention is `datadir/clf_name_experiment-params`, where the params are
    stored in key-value pairs.

    Example of file name: results/IForest-n_estimators_30-bootstrap_True-behaviour_new

    If ground truth labels are provided, then the best estimator is also
    identified and stored separately.

    Parameters
    ----------
    clf : object
        initialized estimator on which to perform parameter tuning.

    params : dictionary
        parameters set for fitting the estimator. Each `fit` argument for the
        estimator should be represented as a list of possible values that
        `GridSearch` will walk using a Cartesian Product generated through
        :class:`~sklearn.model_selection.ParameterGrid`.

        Example:

        .. code-block:: python

            params = {
                'n_estimators': [10, 30, 50, 70, 100, 130, 160, 180, 200, 500],
                'bootstrap': [True, False],
                'behaviour': ['old', 'new'],
            }

        instead of:

        .. code-block:: python

            params = {
                'n_estimators': 10,
                'bootstrap': True,
                'behaviour': 'new',
            }

    clf_type : string, default="sklearn"
        classifier type. Performs workarounds for missing functionalities or API
        compatibilities. For example `tensorflow` can not be `pickle`'d,
        executed in parallel or be `clone`'d.
        Current possible values are `"sklearn"` and `"tensorflow"`.

    datadir : string, default="results"
        directory where to store the trained models and their results for
        each possible parameter configuration provided by the user.
        The directory must exist and is not created by the program.

    n_cpus : int, default=1
        number of processors to use when concurrency or parallelism are
        available.

    get_results : method, default=GridSearch._fpfn
        method that retrieves the restults of one experiment and sets the
        appropiate metrics in `dictionary` format.

        The prototype of the method is `get_results(cls, clf, y_pred, y_true)`.

        The metrics must contain the keys `duration` and `clf`.

        Example
        -------

        .. code-block:: python

            def my_get_results(cls, clf, y_pred, y_true):
                tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
                metrics = {
                    "tn": tn,
                    "fp": fp,
                    "fn": fn,
                    "tp": tp,
                    "duration": 0,
                    "clf": None,
                }
                return metrics

    compare_metric : method, default=GridSearch._compare_metric_balanced_accuracy
        method that compares the current experiment with the best experiment so
        far.

        The prototype of the method is `compare_metric(cls, experiment, clf, metrics)`.

        Returns `True` if current experiment is better and `False` otherwise.

        Example
        -------

        .. code-block:: python

            def ba_compare(cls, experiment, clf, metrics):
                if metrics["ba"] > cls.best_score_["ba"]:
                    return True
                return False


    Attributes
    ----------
    best_estimator_: object
        The best estimator found after `GridSearch` is complete.

    best_params_: dictionary
        The associated parameters of the best estimator.

    best_score_:
        The score obtained by the best estimator.

    best_duration_:
        The duration of the experiment that obtained the best score.

    best_experiment_:
        The name of the best experiment.

    labels_:
         Labels computed by the best estimator.

    estimators_: list
        All the estimators tested during `GridSearch`.

    Example
    -------

    .. code-block:: python

        from graphomaly.grid_search import GridSearch
        from pyod.utils.data import generate_data
        from sklearn.ensemble import IsolationForest

        clf = IsolationForest()
        params = {
            'n_estimators': [10, 30, 50, 70, 100, 130, 160, 180, 200, 500],
            'bootstrap': [True, False],
            'behaviour': ['old', 'new'],
        }
        search = GridSearch(
            clf,
            params,
            n_cpus=4,
            datadir="results",
            clf_type="sklearn",
        )
        X, y = generate_data(train_only=True)
        search.fit(X, y)

    See also
    --------
        tests.test_synthetic_gridsearch: example of performing grid search with
        multiple methods with multiple possible parameters on multiple CPUs
    """

    def __init__(
        self,
        clf,
        params,
        *,
        datadir="results",
        n_cpus=1,
        clf_type="sklearn",
        get_results=None,
        compare_metric=None,
        refit=False,
    ):
        self.base_clf = clf
        self.datadir = datadir
        self.n_cpus = n_cpus
        self.clf_type = clf_type

        self.params = params
        self.refit = refit

        self.clf_name = clf.__class__.__name__

        self.get_results = get_results
        if self.get_results is None:
            self.get_results = _fpfn
        self.compare_metric = compare_metric
        if self.compare_metric is None:
            self.compare_metric = _compare_metric_balanced_accuracy

        # Results
        self.best_estimator_ = None
        self.best_params_ = None
        self.best_score_ = None
        self.best_duration_ = None
        self.best_experiment_ = None
        self.labels_ = None
        self.estimators_ = []

        logging.basicConfig(level=logging.INFO)

    def _compare_results(self, experiment, clf, metrics):
        if self.best_score_ is None:
            self.best_score_ = metrics
            self.best_duration_ = metrics["duration"]
            self.best_experiment_ = experiment
            self.best_estimator_ = clf
            return

        if self.compare_metric(self, experiment, clf, metrics):
            self.best_score_ = metrics
            self.best_duration_ = metrics["duration"]
            self.best_experiment_ = experiment
            self.best_estimator_ = clf

    def _test_clf(self, params):
        X = params.pop("samples")
        y = params.pop("targets")
        start = time.time()

        if self.clf_type == "tensorflow":  # tf has no clone
            clf = self.base_clf
        else:
            clf = clone(self.base_clf)
        clf = clf.set_params(**params)
        y_pred = clf.fit_predict(X)

        metrics = self.get_results(self, clf, y_pred, y)

        end = time.time()
        duration = end - start
        metrics["duration"] = duration

        fname = f"{self.datadir}/{self.clf_name}" + self._experiment_file_params(params)

        if self.clf_type == "tensorflow":  # tf is not pickle compatible
            clf.metrics_ = metrics
            clf.save(fname)
            pickle.dump(
                # [ba, tpr, tnr, duration, tn, fp, fn, tp],
                metrics,
                open(
                    fname + "/metrics",
                    "wb",
                ),
            )
        else:
            metrics["clf"] = clf
            pickle.dump(
                # [clf, ba, tpr, tnr, duration, tn, fp, fn, tp],
                metrics,
                open(
                    fname,
                    "wb",
                ),
            )
        return metrics

    def _grid_make_iterable(self):
        for k, v in self.params.items():
            if not isinstance(self.params[k], Iterable):
                self.params[k] = [v]
            if isinstance(self.params[k], str):
                self.params[k] = [v]

    def _grid_generate_search_space(self, X, y):
        self.params["samples"] = [X]
        self.params["targets"] = [y]
        self._grid_make_iterable()

        self.params = list(ParameterGrid(self.params))

    def _experiment_get_path(self, prefix, p):
        return prefix + self._experiment_file_params(p)

    def _experiment_exists(self, prefix, p):
        experiment = self._experiment_get_path(prefix, p)
        return os.path.isfile(experiment)

    def _experiment_remove_if_exists(self, prefix, p):
        experiment = self._experiment_get_path(prefix, p)
        if os.path.isfile(experiment):
            os.remove(experiment)

    def _experiment_file_params(self, p):
        str_params = ""
        for k, v in p.items():
            if k == "samples" or k == "targets":
                continue
            if type(v) == np.ndarray:
                v = self._params_array_subsample_hash(v)
            str_params += f"-{k}_{v}"
        return str_params

    def _params_array_subsample_hash(self, arr, n_digits=8):
        # inds = np.random.randint(low=0, high=arr.size, size=np.minimum(1000, arr.size))
        # sampled_arr = arr.flat[inds]
        step = np.maximum(1, round(0.1 * arr.size))
        sampled_arr = arr.flat[::step]
        # h = hash(sampled_arr.tobytes())
        # to_hex = hex(abs(h))[2:]  # ditch '0x'
        h = hashlib.sha512()
        h.update(sampled_arr)
        to_hex = h.hexdigest()
        to_str = to_hex[:n_digits]
        return to_str

    def _grid_remove_existing_experiments(self):
        prefix = f"{self.datadir}/{self.clf_name}"
        self.params_in_ = self.params
        for p in self.params:
            self._experiment_remove_if_exists(prefix, p)

    def _grid_remove_existing_tests(self):
        prefix = f"{self.datadir}/{self.clf_name}"
        self.params_in_ = self.params
        self.params = [p for p in self.params if not self._experiment_exists(prefix, p)]

    def _grid_find_best_result(self):
        # p = Path(self.datadir)
        # experiments = list(p.glob(f"{self.clf_name}-*"))
        prefix = f"{self.datadir}/{self.clf_name}"
        experiments = [
            prefix + self._experiment_file_params(p) for p in self.params_in_
        ]
        for i, experiment in enumerate(experiments):
            logging.info(f"{experiment}")
            if os.path.isdir(experiment):  # tf
                clf = load_model(experiment)
                with open(str(experiment) + "/metrics", "rb") as fp:
                    metrics = pickle.load(fp)
            else:
                with open(experiment, "rb") as fp:
                    metrics = pickle.load(fp)
                clf = metrics["clf"]
            self._compare_results(experiment, clf, metrics)

        params = str(self.best_experiment_).split("-")[1:]
        params = ",".join(params)
        logging.info(
            f"{self.clf_name.upper()} BEST [{self.best_duration_:.2f}s]"
            f"({params}): "
            f"{self.best_score_}"
        )

        if hasattr(self.best_estimator_, "get_params"):  # sklearn
            self.best_params_ = self.best_estimator_.get_params()
            self.labels_ = self.best_estimator_.labels_

    def _grid_get_estimators(self):
        p = Path(self.datadir)
        experiments = list(p.glob(f"{self.clf_name}-*"))
        for experiment in experiments:
            with open(experiment, "rb") as fp:
                # [clf, ba, tpr, tnr, duration, tn, fp, fn, tp] = pickle.load(fp)
                metrics = pickle.load(fp)
                clf = metrics["clf"]
                self.estimators_.append(clf)
                print(experiment)
                print(clf)

    def _grid_find_mean_std(self):
        bas = []
        p = Path(self.datadir)
        params = "-".join(str(e[0]) for e in self.params[:-1])  # skip round parameter
        experiments = list(p.glob(f"{self.clf_name}-{params}*"))
        for experiment in experiments:
            with open(experiment, "rb") as fp:
                [ba, tpr, tnr, duration] = pickle.load(fp)
                bas.append(ba)

        max = np.max(bas)
        mean = np.mean(bas)
        std = np.std(bas)
        logging.info(
            f"{self.clf_name.upper()} {len(experiments)} rounds ({params}): "
            f"max {max:.4f}, mean {mean:.4f}, std {std:.4f}"
        )

    def _grid_search(self, X, y):
        self._grid_generate_search_space(X, y)
        if self.refit:
            self._grid_remove_existing_experiments()
        else:
            self._grid_remove_existing_tests()

        # tf incompatible with mp according to tf issue #46316
        if self.n_cpus == 1 or self.clf_type == "tensorflow":
            for p in self.params:
                self._test_clf(p)
        else:
            pool_obj = multiprocessing.Pool(self.n_cpus)
            pool_obj.map(self._test_clf, self.params)

    def fit(self, X, y=None):
        """Perform grid search on samples in `X` with the selected `clf`.

        Parameters
        ----------
        X: array-like of shape (n_samples, n_features)
            samples on which to fit the methods in `models_list`

        y: array-like of shape (n_samples, )
            The ground truth for samples `X`. If `None` then the best estimator
            across parameter options will not be sought.

        Returns
        -------
        self: object
            Fitted estimator.
        """

        self._grid_search(X, y)
        if y is None:
            self._grid_get_estimators()
        else:
            self._grid_find_best_result()

    # def _test_rounds(self, X, y):
    #     self._grid_search(X, y)
    #     self._grid_find_mean_std()


def _fpfn(cls, clf, y_pred, y_true):
    if y_true is None:
        metrics = {
            "ba": None,
            "tpr": None,
            "tnr": None,
            "tn": None,
            "fp": None,
            "fn": None,
            "tp": None,
            "duration": None,
            "clf": None,
        }
        return metrics

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    ba = (tpr + tnr) / 2
    metrics = {
        "ba": ba,
        "tpr": tpr,
        "tnr": tnr,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "duration": 0,
        "clf": None,
    }
    return metrics


def _compare_metric_balanced_accuracy(cls, experiment, clf, metrics):
    if metrics["ba"] > cls.best_score_["ba"]:
        return True
    return False
