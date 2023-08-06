# Copyright (c) 2021 Alexandra Bodirlau <alexandra.bodirlau@tremend.com>, Tremend Software Consulting
# Copyright (c) 2021 Stefania Budulan <stefania.budulan@tremend.com>, Tremend Software Consulting
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

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras.backend as K
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import activations, layers
from tensorflow.keras.regularizers import L2

VAE_ATTRIBUTES = [
    "encoder_neurons",
    "decoder_neurons",
    "input_dim",
    "latent_dim",
    "dropout",
    "activation_function",
    "l2_regularizer",
    "threshold",
    "contamination",
]


@tf.keras.utils.register_keras_serializable()
class VAE(tf.keras.Model):
    """Variational Autoencoder model introduced by Kingma et al. [2]_

    Parameters
    ----------
    encoder_neurons : list
        The number of neurons per encoder layers.

    decoder_neurons : list
        The number of neurons per decoder layers.

    input_dim : int
        The number of features.

    latent_dim : int
        The dimension of the latent space.

    activation_function : str or callable, default='tanh'
        The activation function for all layers.
        See `Keras doc <https://keras.io/api/layers/activations/>`_.

    l2_regularizer : float in (0., 1), default=0.1
        The regularization factor for L2 regularizer for all layers.

    dropout : float in (0., 1), default=0.2
        Dropout rate for all hidden layers.

    threshold : float, default=None
        The threshold used for anomalies selection. If None, the
        contamination is used to compute the threshold.

    contamination : float, default=0.1
        The contamination rate used for computing the reconstruction error
        threshold. Used if threshold is not set.

    Attributes
    ----------
    decision_scores_ : array-like of shape (n_samples,)
        The raw outlier scores for the training data. The anomalies have
        a larger error score.

    history_ : Keras Object
        The training history of the model.

    labels_ : list of integers (0 or 1)
        The binary labels for the training data. 0 means inliers and 1 means
        outliers.

    threshold_ : float
        The threshold for the raw outliers scores.

    References
    ----------
    .. [2] Kingma, Diederik P., and Max Welling. "Auto-encoding variational
        bayes." arXiv preprint arXiv:1312.6114 (2013).
    """

    def __init__(
        self,
        encoder_neurons,
        decoder_neurons,
        input_dim,
        latent_dim,
        activation_function="tanh",
        l2_regularizer=0.1,
        dropout=0.2,
        threshold=None,
        contamination=0.1,
        optimizer=None,
        loss=None,
        epochs=None,
        batch_size=None,
        shuffle=None,
        validation_size=None,
    ):
        super(VAE, self).__init__()

        self.encoder_neurons = encoder_neurons
        self.decoder_neurons = decoder_neurons
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.activation_function = activation_function
        self.l2_regularizer = l2_regularizer
        self.dropout = dropout
        self.contamination = contamination
        self.threshold_ = threshold
        self.scaler = None
        self.decision_scores_ = None
        self.history_ = None
        self.labels_ = None
        self.classes = 2

        self.optimizer = optimizer
        self.loss = loss
        self.epochs = epochs
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.validation_size = validation_size

        self.labels_ = []

        # tf serialization
        self.tf_threshold = tf.Variable(1.0)

        self._check_parameters()
        self._build_model()

    def _build_model(self):
        # Build Encoder
        inputs = layers.Input(shape=(self.input_dim,))
        x = inputs

        for neurons in self.encoder_neurons:
            x = layers.Dense(
                neurons,
                activation=self.activation_function,
                activity_regularizer=L2(self.l2_regularizer),
            )(x)
            x = layers.Dropout(self.dropout)(x)

        z_mean = layers.Dense(self.latent_dim)(x)
        z_log_var = layers.Dense(self.latent_dim)(x)
        z = Sampling()((z_mean, z_log_var))

        self.encoder = tf.keras.Model(inputs, [z_mean, z_log_var, z], name="encoder")

        # Build Decoder
        latent_inputs = layers.Input(shape=(self.latent_dim,))
        outputs = latent_inputs

        for neurons in self.decoder_neurons:
            outputs = layers.Dense(
                neurons,
                activation=self.activation_function,
                activity_regularizer=L2(self.l2_regularizer),
            )(outputs)
            outputs = layers.Dropout(self.dropout)(outputs)

        self.decoder = tf.keras.Model(latent_inputs, outputs, name="decoder")

    def call(self, inputs):
        if inputs.shape[1] != self.decoder_neurons[-1]:
            raise ValueError(
                "Expected the number of features to be equal to "
                "the number of neurons on the last decoder layer. "
                f"But found: {inputs.shape[1]} features and "
                f"{self.decoder_neurons[-1]} neurons."
            )

        # encoder
        z_mean, z_log_var, z = self.encoder(inputs)
        reconstructed = self.decoder(z)

        # Add KL divergence regularization loss.
        kl_loss = -0.5 * tf.reduce_mean(
            z_log_var - tf.square(z_mean) - tf.exp(z_log_var) + 1
        )
        self.add_loss(kl_loss)
        return reconstructed

    def summary(self):
        """Print Autoencoder architecture on components."""
        print(self.encoder.summary())
        print(self.decoder.summary())

    def predict_decision_scores(self, X_train):
        """Predict the reconstruction errors for the samples on which the model
        was trained. The anomalies have a larger error score.

        These scores are used to fit the scaler used by
        predict_proba() method.

        Parameters
        ----------
        X_train : array-like of shape (num_samples, num_features)
            The train samples.

        Returns
        -------
        ndarray of shape (num_samples, )
            The reconstruction error scores.

        """
        preds = super().predict(X_train)

        self.decision_scores_ = self._compute_scores(X_train, preds)
        self.scaler = MinMaxScaler()
        self.scaler.fit(self.decision_scores_.reshape(-1, 1))

        if self.threshold_ is None:
            self.threshold_ = pd.Series(self.decision_scores_).quantile(
                1 - self.contamination
            )

        self.labels_ = (self.decision_scores_ > self.threshold_).astype("int")
        self.tf_threshold.assign(self.threshold_)

        return self.decision_scores_

    def decision_function(self, X):
        """Predict the reconstruction errors for some samples.
        The anomalies have a larger error score.

        Parameters
        ----------
        X : array-like of shape (num_samples, num_features)
            The samples for which to compute the scores.

        Returns
        -------
        ndarray of shape (num_samples, )
            The reconstruction error scores.

        """
        preds = super().predict(X)
        return self._compute_scores(X, preds)

    def predict_proba(self, X, method="linear"):
        """Compute a distribution probability on the reconstuction errors
        predicted for the samples passed as parameter. The scores as normalized
        using a scaler fitted on the train scores, so the method
        predict_train_scores() must be called after training the model in order
        to be able to compute the probabilities.

        Parameters
        ----------
        X : array-like of shape (num_samples, num_features)
            The samples for which to compute the probabilities.

        method : {'linear'}, default='linear'
            The method used for score normalization. Only 'linear' supported at
            the moment.

        Returns
        -------
        ndarray of shape (num_samples, )
            The probabilities for each class (normal prob on dimension 0,
            anomaly prob on dimension 1).

        """
        if self.decision_scores_ is None:
            raise Exception(
                "Train scores weren't computed. Please call "
                "predict_decision_scores(), then retry."
            )

        scores = self.decision_function(X)
        probs = np.zeros([X.shape[0], self.classes])

        if method == "linear":
            probs[:, 1] = self.scaler.transform(scores.reshape(-1, 1)).squeeze()
            probs[:, 0] = 1 - probs[:, 1]

        else:
            raise ValueError(
                f"{method} is not a valid value for probability" "conversion."
            )

        return probs

    def set_params(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def get_params(self, deep=True):
        return {
            "encoder_neurons": self.encoder_neurons,
            "decoder_neurons": self.decoder_neurons,
            "input_dim": self.input_dim,
            "latent_dim": self.latent_dim,
            "activation_function": self.activation_function,
            "l2_regularizer": self.l2_regularizer,
            "dropout": self.dropout,
            "contamination": self.contamination,
            "threshold": self.threshold_,
            "optimizer": self.optimizer,
            "loss": self.loss,
            "epochs": self.epochs,
            "batch_size": self.batch_size,
            "shuffle": self.shuffle,
            "validation_size": self.validation_size,
        }

    def fit(self, X, y=None, **kwargs):
        self.set_params(**kwargs)

        self.compile(optimizer=self.optimizer, loss=self.loss)

        self.history_ = (
            super()
            .fit(
                X,
                X,
                epochs=self.epochs,
                batch_size=self.batch_size,
                validation_split=self.validation_size,
                shuffle=self.shuffle,
                verbose=self.verbose,
            )
            .history
        )

        self.predict_decision_scores(X)

        return self

    def predict(self, X):
        """Predict binary labels for the samples passed as parameter.

        Parameters
        ----------
        X : array-like of shape (num_samples, num_features)
            The samples for which to compute the probabilities.

        Returns
        -------
        ndarray of shape (num_samples, )
            The probabilities for each class.
        """

        pred_score = self.decision_function(X)
        self.labels_ = (pred_score > self.threshold_).astype("int")
        return self.labels_

    def fit_predict(self, X, y=None):
        return self.fit(X, y).predict(X)

    def _check_parameters(self):
        if not isinstance(self.encoder_neurons, list):
            raise TypeError(
                "Expected encoder_neurons to have type list, but "
                f"received {type(self.encoder_neurons)}"
            )

        if not isinstance(self.decoder_neurons, list):
            raise TypeError(
                "Expected decoder_neurons to have type list, but "
                f"received {type(self.encoder_neurons)}"
            )

        if not all(map(lambda x: isinstance(x, int), self.encoder_neurons)):
            raise TypeError("Not all elements from encoder_neurons have int " "type")

        if not all(map(lambda x: isinstance(x, int), self.decoder_neurons)):
            raise TypeError("Not all elements from decoder_neurons have int " "type")

        # Check regularizer type and value
        if not isinstance(self.l2_regularizer, float):
            raise TypeError(
                "Expected l2_regularizer to have type float, but "
                f"received {type(self.l2_regularizer)}"
            )

        if self.l2_regularizer < 0.0 or self.l2_regularizer > 1.0:
            raise ValueError(
                "Expected l2_regularizer to have a value in (0.0,"
                f"1.0) range, but received {self.l2_regularizer}"
            )

        # Check activation_function value and type
        if isinstance(self.activation_function, str):
            try:
                activations.deserialize(str(self.activation_function))
            except ValueError:
                raise ValueError(
                    "activation_function value is not supported. "
                    "Please check: https://keras.io/api/layers/activations/"
                    " for available values."
                )

        elif not isinstance(self.activation_function, callable):
            raise TypeError(
                "Expected activation_function to be str or "
                "callable. Please check: "
                "https://keras.io/api/layers/activations/ for "
                "available values."
            )

        if self.contamination is None and self.threshold_ is None:
            raise TypeError(
                "Expected 'contamination' or 'threshold_' to "
                "be float, but received None."
            )

        # Check input dimensions
        if self.input_dim != self.decoder_neurons[-1]:
            raise ValueError(
                "Expected 'input_dim' to be equal to the number "
                "of neurons on the last decoder layer. But received: "
                f"{self.input_dim} input dimension and "
                f"{self.decoder_neurons[-1]} neurons."
            )

    @classmethod
    def _compute_scores(cls, X, Y):
        return np.sqrt(np.sum(np.square(Y - X), axis=1))


class Sampling(layers.Layer):
    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = K.shape(z_mean)[0]  # batch size
        dim = K.int_shape(z_mean)[1]  # latent dimension
        epsilon = K.random_normal(shape=(batch, dim))  # mean=0, std=1.0

        return z_mean + K.exp(0.5 * z_log_var) * epsilon
