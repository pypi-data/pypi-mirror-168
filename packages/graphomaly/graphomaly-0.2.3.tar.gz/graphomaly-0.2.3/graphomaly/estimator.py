# Copyright (c) 2021, 2022 Paul Irofti <paul@irofti.net>
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

import logging
import os

import networkx as nx
import numpy as np
import pandas as pd
import yaml
from attrdict import AttrDict
from sklearn.base import BaseEstimator

from .grid_search import GridSearch
from .models import ModelsLoader
from .preprocessing.egonet import EgonetFeatures
from .preprocessing.rwalk import RwalkFeatures
from .preprocessing.spectrum import SpectrumFeatures
from .preprocessing.transactions_to_graph import Transactions2Graph
from .voting import VotingClassifier


class GraphomalyEstimator(BaseEstimator):
    """Anomaly detection in graphs.

    The estimator expects a dataset with an underlying graph structure
    and a set of machine learning models and associated parameters
    on which to perform parameter tuning via grid search techniques.
    The result is an ensemble of optimized machine learning models that
    provides labels on existing and new incoming data via voting methods.

    Parameters
    ----------
    config_file: string, default="graphomaly.yaml"
        user provided configuration file that will overwrite the constructor
        provided parameters.

    models_train_all: bool, default=False
        if `True`, performs training on all available models. See
        `ModelsLoader` from `graphomaly.models` for a full list.

    models_subset: list, default=["PyodIForest", "PyodLOF", "PyodOCSVM"]
        if `models_train_all` is `False`, the list of machine learning models to
        use for the Graphomaly estimator.

    models_ctor_kwargs: dictionary, default=None
        constructor arguments for each of the selected machine learning models.

    models_fit_kwargs: dictionary, default=None
        :meth:`fit` arguments for each of the selected machine learning models.

    n_cpus: int, default=1
        number of processors to use when concurrency and parallelism is
        available. Also used during `GridSearch` inside
        `graphomaly.grid_search`.

    results_path: string, default="results"
        directory where to store the trained models for each possible parameter
        configuration provided by the user. The directory is created if it does
        not exist.

    voting: string, default="hard"
        voting method to use for perdictions with the resulting ensemble. See
        the `VotingClassifier` from `graphomaly.voting` for more details.

    Attributes
    ----------
    config: attrdict
        if `config_file` was used, this contains the read configuration parameters

    config_file: string
        user provided configuration file

    models_train_all: bool
        whether all available models were used during training

    models_subset: list
        subset of machine learning models to use during training

    models_ctor_kwargs: dictionary
        constructor arguments used for each of the selected machine learning models

    models_fit_kwargs: dictionary
        :meth:`fit` arguments used for each of the selected machine learning models

    n_cpus: int
        number of processors to use

    results_path: string
        directory where trained models are stored

    voting: string
        voting method to used for predictions

    labels_: ndarray
        resulting labels after ensemble voting

    models_list: tuple
        list of models resulting after handling `models_train_all` and `models_subset`
        user options. Used together with `models` when labels are available
        during `GridSearch`

    models: list
        trained models objects for each method in `models_list`. This will
        include the models that performed best during `GridSearch` if labels
        were available during :meth:`fit`, or the models for all parametrizations
        if labels were not available during :meth:`fit`.

    models_name: list
        used together with `models` when labels are not available during `GridSearch`

    feature_names_in_: list
        used during graph preprocessing to store features names

    best_estimators: dict
        best estimator resulted during `GridSearch` for each model

    best_labels_: dict
        associated labels for best estimators resulted during `GridSearch`
        for each model

    best_params: dict
        associated parametrization for best estimators resulted during `GridSearch`
        for each model

    best_score_:  dict
        associated score for best estimators resulted during `GridSearch`
        for each model
    """

    def __init__(
        self,
        config_file="graphomaly.yaml",
        models_train_all=False,
        models_subset=["PyodIForest", "PyodLOF", "PyodOCSVM"],
        models_ctor_kwargs=None,
        models_fit_kwargs=None,
        n_cpus=1,
        results_path="results",
        voting="hard",
    ):
        self.config_file = config_file
        self.models_train_all = models_train_all
        self.models_subset = models_subset
        self.models_ctor_kwargs = models_ctor_kwargs
        self.models_fit_kwargs = models_fit_kwargs
        self.n_cpus = n_cpus
        self.results_path = results_path
        self.voting = voting

        self.labels_ = []

        self.models_list = []
        self.models = []
        self.models_name = []
        self.feature_names_in_ = []

        self._model_is_fitted = False

        # tune
        self.best_estimators = {}
        self.best_labels_ = {}
        self.best_params = {}
        self.best_score_ = {}

        logging.basicConfig(level=logging.INFO)

        # Overwrite from configuration file
        if self.config_file and os.path.exists(self.config_file):
            with open(self.config_file) as f:
                self.config = AttrDict(yaml.safe_load(f))

                self.models_train_all = self.config.models.train_all
                self.models_subset = self.config.models.subset
                self.models_ctor_kwargs = self.config.models.ctor_kwargs
                self.models_fit_kwargs = self.config.models.fit_kwargs
                self.results_path = self.config.results.path
                self.voting = self.config.voting

        os.makedirs(self.results_path, exist_ok=True)

        self._get_models_list()

    def load(self):
        """Virtual method for loading the dataset."""
        raise NotImplementedError("Must override load() for your dataset")

    def preprocess(self, X, y, type=None, **kwargs):
        """Apply preprocessing operations on raw dataset.

        Parameters
        ----------
        X: array-like of shape (n_samples, n_features)
            The raw training dataset consisting of transactions list or graph

        y: array-like of shape (n_samples, )
            The ground truth for training dataset.

        type: string
            Preprocessing steps required. Depending on the input, the possible
            preprocessing actions are:

            * `'transactions_to_features'`: see  :ref:`sec-transaction-list-to-features` (TODO)
            * `'graph_to_features'`: see :ref:`sec-graph-to-features`
            * `'transactions_to_graph_to_features'`: combines the operations from
                :ref:`sec-transaction-list-to-graph` and :ref:`sec-graph-to-features`

        Keyword Args: dictionary
            The keyword args contains a dictionary consisting of two entries

            * to_graph_args: dictionary
                Contains fit `kwargs` for `preprocessing.transactions_to_graph`
                module
            * to_feature_args: dictionary
                Available key values:

                * algorithms: list of strings
                    Possible elements: `'egonet'`, `'rwalk'`, `'spectrum'`
                * algorithms_args: dictionary
                    Possible elements: '`ctor_args'` and `'fit_args'`

                    * ctor_args: dictionary
                        Represents arguments passed to the algorithm's constructor.
                    * fit_args: dictionary
                        Represents options passed to the fit method.

        Returns
        -------
        X: ndarray
            The preprocessed training dataset.

        y: ndarray
            The preprocessed labels.

        G: ndarray
            The graph associated to the raw training dataset.

        See also
        --------
        tests.test_synthetic_preprocessing : example of building and passing kwargs
        """
        G = None

        # if type == "transactions_to_features":
        if type == "graph_to_features":
            if y is not None:
                y = self._preprocess_labels(X, y, type)
            X = self._process_graph_to_features(X, **kwargs)
        elif type == "transactions_to_graph_to_features":
            to_graph_args = kwargs["to_graph_args"]
            to_features_args = kwargs["to_features_args"]

            if y is not None:
                y = self._preprocess_labels(X, y, type)
            t2g = Transactions2Graph()
            G = t2g.fit_transform(X, **to_graph_args)

            X = self._process_graph_to_features(G, **to_features_args)
        return X, y, G

    def _preprocess_labels(self, X, y, type):
        if type == "transactions_to_graph_to_features" or type == "graph_to_features":
            Xy = np.c_[X[:, 0], X[:, 1], y]
            Xy = pd.DataFrame(data=Xy, columns=["source", "destination", "labels"])

            gXy = nx.from_pandas_edgelist(
                df=Xy,
                source="source",
                target="destination",
                edge_attr=True,
                create_using=nx.MultiDiGraph,
            )

            y_true_nodes = np.zeros((gXy.number_of_nodes(),), dtype=int)
            nodes_array = np.array(gXy.nodes())
            for (i, j, label) in gXy.edges.data("labels"):
                if label >= 1:
                    index = np.where(nodes_array == i)[0][0]
                    y_true_nodes[index] = 1
                    index = np.where(nodes_array == j)[0][0]
                    y_true_nodes[index] = 1

            # sort on node id
            ii = np.argsort(nodes_array)
            y = y_true_nodes[ii]

        return y

    def _process_graph_to_features(self, G, **kwargs):
        algorithms = kwargs["graph_algorithms"]
        algorithms_args = kwargs["graph_algorithms_args"]

        all_features = []
        for i, algo in enumerate(algorithms):
            ctor_args = algorithms_args[i]["ctor_args"]
            fit_args = algorithms_args[i]["fit_args"]
            if algo == "egonet":
                ego = EgonetFeatures(**ctor_args)
                features = ego.fit_transform(G, **fit_args)
                features_names_in = ego.feature_names_in_
            elif algo == "rwalk":
                rwalk = RwalkFeatures(**ctor_args)
                features = rwalk.fit_transform(G, **fit_args)
                features_names_in = rwalk.feature_names_in_
            elif algo == "spectrum":
                spectrum = SpectrumFeatures(**ctor_args)
                features = spectrum.fit_transform(G, **fit_args)
                features_names_in = spectrum.feature_names_in_
            all_features.append(features)
            self.feature_names_in_.append(features_names_in)

        return np.concatenate(all_features, axis=1)

    def _get_params(self, algorithm, n_features):
        model_kwargs = {}
        if self.models_ctor_kwargs is not None:
            if algorithm in self.models_ctor_kwargs:
                model_kwargs = self.models_ctor_kwargs[algorithm]

        fit_kwargs = {}
        if self.models_fit_kwargs is not None:
            if algorithm in self.models_fit_kwargs:
                fit_kwargs = self.models_fit_kwargs[algorithm]

        # Setting the correct number of decoder neurons after preprocessing.
        if "decoder_neurons" in model_kwargs:
            model_kwargs["decoder_neurons"][-1] = n_features

        if "input_dim" in model_kwargs:
            model_kwargs["input_dim"] = n_features

        return model_kwargs, fit_kwargs

    def _get_models_list(self):
        if self.models_train_all:
            self.models_list = ModelsLoader.models
        else:
            self.models_list = self.models_subset

    def fit(self, X, y=None):
        """Perform anomaly detection on samples in `X`.

        Parameters
        ----------
        X: array-like of shape (n_samples, n_features)
            samples on which to fit the methods in `models_list`

        y: array-like of shape (n_samples, )
            The ground truth for samples `X`. If `None` then the best estimator
            across parameter opotions will not be sought.

        Returns
        -------
        self: object
            Fitted estimator.

        See also
        --------
        tests.test_synthetic:
            example of performing fit on synthetic
            generated data on a small subset of methods and parameters list.
        """
        if self._model_is_fitted is True:
            return self

        self.tune(X, y)
        self._model_is_fitted = True

        return self

    def refit(self, X, y=None):
        """Retrain anomaly detection models on samples in `X`.

        Parameters
        ----------
        X: array-like of shape (n_samples, n_features)
            samples on which to fit the methods in `models_list`

        y: array-like of shape (n_samples, )
            The ground truth for samples `X`. If `None` then the best estimator
            across parameter opotions will not be sought.

        Returns
        -------
        self: object
            Re-Fitted estimator.
        """
        if self._model_is_fitted is False:
            return

        self.tune(X, y, refit=True)

    def predict(self, X, y=None, voting=None):
        """Perform anomaly detection on samples in `X`.

        A wrapper around `vote`. Labels are also stored in `self.labels_`.

        Parameters
        ----------
        X: array-like of shape (n_samples, n_features)
            samples on which to perform anomaly detection

        y: array-like of shape (n_samples, )
            The ground truth for samples `X`

        voting: string
            Voting method. See `graphomaly.voting` for available options.

        Returns
        -------
        y: array-like of shape (n_samples, )
            The predicted labels

        See also
        --------
        tests.test_synthetic: example of predicting on synthetic generated data.
        """
        self.labels_ = self.vote(X, y, voting)
        return self.labels_

    def vote(self, X, y=None, voting=None):
        """Perform anomaly detection on samples in `X` using Graphomaly's
        `VotingClassifier`.

        Parameters
        ----------
        X: array-like of shape (n_samples, n_features)
            samples on which to perform anomaly detection

        y: array-like of shape (n_samples, )
            The ground truth for samples `X`

        voting: string
            Voting method. See `graphomaly.voting` for available options.

        Returns
        -------
        y: array-like of shape (n_samples, )
            The predicted labels

        See also
        --------
        tests.test_synthetic_voting:
            example of trying all available voting methods
        """
        if voting:
            self.voting = voting
        if self.known_best_estimator:
            estimators = [(i, j) for i, j in zip(self.models_list, self.models)]
        else:
            estimators = [(i, j) for i, j in zip(self.models_name, self.models)]
        eclf = VotingClassifier(estimators=estimators, voting=self.voting)
        y = eclf.fit_predict(X, y)
        return y

    def tune(self, X, y=None, refit=False):
        """Perform parameter tuning on samples in `X` using Graphomaly's
        `GridSearch`.

        Parameters
        ----------
        X: array-like of shape (n_samples, n_features)
            samples on which to perform parameter tuning for the `models_list`

        y: array-like of shape (n_samples, )
            The ground truth for samples `X`. If `None` then the best estimator
            information will not be set.

        refit: bool, default=False
            If this is a refit, clean existing model before proceeding with
            GridSearch.

        Returns
        -------
        self: object
            Fitted estimator.

        See also
        --------
        tests.test_synthetic_gridsearch:
            example of performing parameter tuning
            on a small subset of methods and parameters list.
        """
        for algorithm in self.models_list:
            model_kwargs, fit_kwargs = self._get_params(algorithm, X.shape[1])
            clf = ModelsLoader.get(algorithm, **model_kwargs)
            if hasattr(clf, "save"):  # tf model detected
                clf_type = "tensorflow"
            else:
                clf_type = "sklearn"

            search = GridSearch(
                clf,
                fit_kwargs,
                n_cpus=self.n_cpus,
                datadir=self.results_path,
                clf_type=clf_type,
                refit=refit,
            )
            search.fit(X, y)

            if y is None:
                self.models_name.extend([algorithm])
                self.models.extend(search.estimators_)
                self.known_best_estimator = False
            else:
                self.best_params[algorithm] = search.best_params_
                self.best_estimators[algorithm] = search.best_estimator_
                self.best_labels_[algorithm] = search.labels_
                self.best_score_[algorithm] = search.best_score_
                self.known_best_estimator = True

                self.models.append(search.best_estimator_)

                logging.info(
                    f"Best params for {algorithm}[{search.best_score_}]: "
                    f"{search.best_params_}"
                )

        return self
