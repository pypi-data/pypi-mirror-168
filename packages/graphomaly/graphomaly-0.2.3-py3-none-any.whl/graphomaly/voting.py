# Copyright (c) 2022 Andra Băltoiu <andra.baltoiu@gmail.com>
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

import inspect

import numpy as np
from pyod.models.combination import aom, average, maximization, median, moa
from pyod.utils.utility import standardizer
from sklearn.base import ClassifierMixin
from sklearn.ensemble._voting import _BaseVoting
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils.metaestimators import available_if
from sklearn.utils.validation import check_is_fitted


class VotingClassifier(ClassifierMixin, _BaseVoting):
    def __init__(
        self,
        estimators,
        *,
        voting="hard",
        weights=None,
        n_jobs=None,
        flatten_transform=True,
        verbose=False,
    ):
        super().__init__(estimators=estimators)
        self.voting = voting
        self.weights = weights
        self.n_jobs = n_jobs
        self.flatten_transform = flatten_transform
        self.verbose = verbose

        self.estimators_ = []

    def fit(self, X, y=None):
        # clf = self.estimators[:][1]

        for name, clf in enumerate(self.estimators):
            if self._model_is_fitted(clf[1], X[0]):
                self.estimators_.append(clf[1])
                continue
            self.estimators[name] = clf[1].fit(X)
            self.estimators_.append(clf[1])

        self.__sklearn_is_fitted__()
        return self

    def _model_is_fitted(self, model, X):
        """Checks if model object has any attributes ending with an underscore.

        Notes
        -----
        **References:**
        Scikit-learn glossary on `fitted'
        https://scikit-learn.org/dev/glossary.html#term-fitted

        Stack-Overflow answer for the best way to check if a model is fitted.
        https://stackoverflow.com/a/48046685
        """
        try:
            return 0 < len(
                [
                    k
                    for k, v in inspect.getmembers(model)
                    if k.endswith("_") and not k.startswith("__")
                ]
            )
        except ValueError:  # keras compiled model
            try:
                model.predict(X[None, :])  # expecting a single vector
                return True
            except NotFittedError:
                return False

    def __sklearn_is_fitted__(self) -> bool:
        return getattr(self, "fitted_", True)

    def __fix_saved_tf_scores(self, X, method):
        clf = method[1]
        if "Custom>Autoencoder" in str(type(method[1])):
            from graphomaly.models.autoencoder import Autoencoder

            Y = clf.predict(X)
            scores = Autoencoder._compute_scores(X, Y)
        elif "Custom>VAE" in str(type(method[1])):
            from graphomaly.models.vae import VAE

            Y = clf.predict(X)
            scores = VAE._compute_scores(X, Y)
        else:
            scores = clf.predict(X)  # i.e. give-up!

        labels = (scores > clf.tf_threshold.numpy()).astype("int")

        scaler = MinMaxScaler()
        scaler.fit(scores.reshape(-1, 1))
        probs = np.zeros([X.shape[0], 2])
        probs[:, 1] = scaler.transform(scores.reshape(-1, 1)).squeeze()
        probs[:, 0] = 1 - probs[:, 1]

        return scores, labels, probs

    def predict(self, X):
        check_is_fitted(self)

        # for pyod methods, compute scores
        if self.voting != "soft" and self.voting != "hard":
            scores = []
            for method in self.estimators:
                try:
                    method_scores = method[1].decision_function(X)
                except AttributeError:
                    method_scores, _, _ = self.__fix_saved_tf_scores(X, method)
                scores.append(method_scores)
            scores_norm = standardizer(np.transpose(scores))

        # soft and hard votings from sklearn
        if self.voting == "soft":
            maj = np.argmax(self.predict_proba(X), axis=1)
            #  maj = self.le_.inverse_transform(maj)

        elif self.voting == "hard":  # 'hard' voting
            predictions = self._predict(X)
            maj = np.apply_along_axis(
                lambda x: np.argmax(np.bincount(x, weights=self._weights_not_none)),
                axis=1,
                arr=predictions,
            )
            #  maj = self.le_.inverse_transform(maj)

        elif self.voting == "average":
            maj = average(scores_norm)
        elif self.voting == "maximization":
            maj = maximization(scores_norm)
        elif self.voting == "median":
            maj = median(scores_norm)
        elif self.voting == "aom":
            maj = aom(scores_norm, int(len(self.estimators_) / 2))
        elif self.voting == "moa":
            maj = moa(scores_norm, int(len(self.estimators_) / 2))

        return maj

    def fit_predict(self, X, y):
        return self.fit(X, y).predict(X)

    def _collect_probas(self, X):
        """Collect results from clf.predict calls."""
        # return np.asarray([clf.predict_proba(X) for clf in self.estimators_])
        probas = []
        for method in self.estimators:
            try:
                probas_pred = method[1].predict_proba(X)
            except AttributeError:
                _, _, probas_pred = self.__fix_saved_tf_scores(X, method)
            probas.append(probas_pred)
        return np.asarray(probas, dtype="float32")

    def _check_voting(self):
        if self.voting == "hard":
            raise AttributeError(
                f"predict_proba is not available when voting={repr(self.voting)}"
            )
        return True

    def _predict(self, X):
        y = []
        for method in self.estimators:
            y_pred = method[1].predict(X)
            if y_pred.ndim > 1:  # saved tf autoencoders
                _, y_pred, _ = self.__fix_saved_tf_scores(X, method)
            y.append(y_pred)
        return np.asarray(y, dtype="int").T

    @available_if(_check_voting)
    def predict_proba(self, X):
        """Compute probabilities of possible outcomes for samples in X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        avg : array-like of shape (n_samples, n_classes)
            Weighted average probability for each class per sample.
        """
        check_is_fitted(self)
        avg = np.average(
            self._collect_probas(X), axis=0, weights=self._weights_not_none
        )
        return avg

    def transform(self, X):
        """Return class labels or probabilities for X for each estimator.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Training vectors, where `n_samples` is the number of samples and
            `n_features` is the number of features.

        Returns
        -------
        probabilities_or_labels
            If `voting='soft'` and `flatten_transform=True`:
                returns ndarray of shape (n_classifiers, n_samples *
                n_classes), being class probabilities calculated by each
                classifier.
            If `voting='soft' and `flatten_transform=False`:
                ndarray of shape (n_classifiers, n_samples, n_classes)
            If `voting='hard'`:
                ndarray of shape (n_samples, n_classifiers), being
                class labels predicted by each classifier.
        """
        check_is_fitted(self)

        if self.voting == "soft":
            probas = self._collect_probas(X)
            if not self.flatten_transform:
                return probas
            return np.hstack(probas)

        else:
            return self._predict(X)
