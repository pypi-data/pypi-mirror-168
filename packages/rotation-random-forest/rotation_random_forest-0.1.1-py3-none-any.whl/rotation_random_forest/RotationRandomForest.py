from typing import List, Union

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from RotationTree import RotationTree


class RotationForest:
    """Forest with RotationTree as base estimator.

    Algorithm:
    Building n_estimator of RotationTree.

    Args:
        n_estimators (int, optional): Number of estimator in forest.
        k_features_subsets (int, optional): Number of feature subsets.
        random_state (int, optional): Seed of random to use. Defaults to 73.

    Methods:
        fit(np.ndarray, np.ndarray): fitting the forest.
        predict(np.ndarray): make predictions on new data.
        predict_proba(np.ndarray): make predictions of probability on new data.
        score (np.ndarray, np.ndarray): calculate accuracy_score.

    Example:
    >>> from sklearn.datasets import make_classification
    >>> X, y = make_classification(
    ...     n_samples=100, n_features=20, n_classes=2,
    ...     n_informative=4, n_redundant=3, n_repeated=2,
    ...     random_state=42)
    >>> rrf = RotationForest(100, 2)
    >>> rff = rrf.fit(X, y)
    """

    def __init__(
        self,
        n_estimators: int = 100,
        k_features_subsets: int = 2,
        random_state=None,
        **fit_params
    ):
        self.n_estimators = n_estimators
        self.k_features_subsets = k_features_subsets
        self.random_state = random_state
        self.fit_params = fit_params
        self.models: List[RotationTree] = list()

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fitting the forest.

        Args:
            X (np.ndarray): Matrix of data
            y (np.ndarray): vector of y_true
        """

        X = self.__pd_data(X)
        for _ in range(self.n_estimators):
            model = RotationTree(
                self.k_features_subsets,
                random_state=self.random_state,
                **self.fit_params
            )
            model.fit(X, y)
            self.models.append(model)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions for new data.

        Args:
            X (np.ndarray): Matrix of data

        Returns:
            np.ndarray: vector of predictions
        """

        predictions = list()
        for model in self.models:
            pred = model.predict(X)
            predictions.append(pred)
        predictions_ = np.array(predictions)

        final_pred = []
        for i in range(len(X)):
            pred_from_all_models = np.ravel(predictions_[:, i])
            frequency = np.bincount(pred_from_all_models.astype("int"))
            final_pred.append(np.argmax(frequency))

        return np.array(final_pred)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Make probability predictions for new data.

        Args:
            X (np.ndarray): Data matrix

        Returns:
            np.ndarray: matrix of probability for every class
        """

        predictions = []
        for model in self.models:
            pred = model.predict_proba(X)
            predictions.append(pred)

        predictions_ = np.array(predictions)

        final_pred = np.zeros((predictions_.shape[1], predictions_.shape[2]))
        for i in range(len(X)):
            final_pred[i, 0] = predictions_[:, i, 0].mean()
            final_pred[i, 1] = predictions_[:, i, 1].mean()

        return final_pred

    def score(self, X: np.ndarray, y: np.ndarray):
        """accuracy_score

        Args:
            X (np.ndarray): data matrix
            y (np.ndarray): y_true vector

        Returns:
            float: accuracy
        """

        pred = self.predict(X)
        return accuracy_score(y, pred)

    @staticmethod
    def __pd_data(X: Union[np.ndarray, pd.DataFrame]) -> pd.DataFrame:
        """Returns pandas DataFrame for right work of algorithm.

        Args:
            data (np.array): Input values.

        Returns:
            pd.DataFrame
        """

        if isinstance(X, np.ndarray):
            return pd.DataFrame(X)
        return X


if __name__ == "__main__":
    import doctest

    doctest.testmod()
