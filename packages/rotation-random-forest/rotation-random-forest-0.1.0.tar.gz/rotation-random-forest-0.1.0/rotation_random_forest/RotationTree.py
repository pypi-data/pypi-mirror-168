from typing import Iterable, List

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier


class RotationTree:
    """Base estimator for RotaionForest.

    Algorithm:
    Split feature set into k features subsets.
    For every subset select a bootstrap sample from X of size 75% of the number of objects in X.
    Apply PCA on this bootstrap sample and add PCA.components_ to the rotation matrix.
    Then build tree using regenerated bootstrap sample multiplied by the rotation matrix

    Args:
        k_features_subsets (int, optional): Number of the feature subsets.
        random_state (int, optional): Seed of random to use. Defaults to 73.

    Attrs:
        rotation_matrix (np.ndarray): rotation matrix to rotate the data.

    Methods:
        fit(pd.DataFrame, pd.DataFrame): fitting the estimator.
        predict(pd.DataFrame): make predictions on new data.
        predict_proba(pd.DataFrame): make predictions of probability on new data.
    """

    def __init__(
        self, k_features_subsets: int = 5, random_state: int = None, **fit_params
    ):
        self.model = DecisionTreeClassifier(random_state=random_state, **fit_params)

        self.random_state = random_state
        self.k_features_subsets = k_features_subsets
        np.random.seed(random_state)

    def fit(self, X: pd.DataFrame, y: pd.DataFrame) -> object:
        """Fitting estimator

        Args:
            X (pd.DataFrame): Data
            y (pd.DataFrame): True labels

        Raises:
            ValueError: if k_features_subsets > features in data

        Returns:
            object: self
        """

        if self.k_features_subsets > X.shape[1]:
            raise ValueError(
                "'k_features_subsets must be less than number of features in data.'"
            )

        feature_subsets = self.get_subsets(X)

        self.rotation_matrix = np.zeros((X.shape[1], X.shape[1]), dtype=float)

        pca = PCA(random_state=self.random_state)

        for subset in feature_subsets:
            bt_sample = self.get_sample(X, subset)
            pca.fit(bt_sample)
            self.update_rotation_matrix(subset, pca.components_)

        X_train, y_train = self.get_boot_sample(X, y)
        X_transformed = X_train.dot(self.rotation_matrix)
        self.model.fit(X_transformed, y_train)

        return self

    def get_subsets(self, X: pd.DataFrame) -> list:
        """Make k disjoint subsets of features.

        Args:
            X (pd.DataFrame): data

        Returns:
            list: list of k subsets
        """

        n_features = X.shape[1]
        features_set = list(range(n_features))
        np.random.shuffle(
            features_set,
        )
        m = n_features // self.k_features_subsets

        subsets = [
            [
                feature
                for feature in features_set[
                    i : self.k_features_subsets * m : self.k_features_subsets
                ]
            ]
            for i in range(self.k_features_subsets)
        ]

        return subsets

    def get_sample(
        self, X: pd.DataFrame, features: Iterable[int], bt_prcnt: float = 0.75
    ) -> pd.DataFrame:
        """Sample with features and 0.75 size of X.shape[0] for PCA fitting.

        Args:
            X (pd.DataFrame): data
            features (Iterable[int]): indexes of features to take
            bt_prcnt (int, optional): Size of bootstrap sample. Defaults to 0.75.

        Returns:
            pd.DataFrame: bootstrap sample
        """

        subset_obj_idx = np.random.choice(
            list(range(X.shape[0])),
            size=int(bt_prcnt * X.shape[0]),
        )

        return X.iloc[subset_obj_idx, features]

    def update_rotation_matrix(self, subset: List[int], pca_components) -> None:
        """Update the rotation matrix with pca's components.

        Args:
            subset (Iterable[int]): indexes of features to update
            pca_components (Iterable[Iterable[int]]): pca's components
        """
        for i in range(0, len(pca_components)):
            for j in range(0, len(pca_components)):
                self.rotation_matrix[subset[i], subset[j]] = pca_components[i, j]

    def get_boot_sample(self, X: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
        newdata = np.concatenate((X, y[:, np.newaxis]), axis=1)
        cases = np.random.choice(
            newdata.shape[0],
            size=newdata.shape[0],
            replace=True,
        )
        samples = newdata[
            cases,
        ]

        return samples[:, :-1], samples[:, -1]

    def predict(self, X: pd.DataFrame):
        """Predict for new data.

        Args:
            X (pd.DataFrame): data

        Returns:
            np.ndarray: model output
        """
        X_transformed = X.dot(self.rotation_matrix)
        return self.model.predict(X_transformed)

    def predict_proba(self, X: pd.DataFrame):
        """Probability predictions for new data.

        Args:
            X (pd.DataFrame): data

        Returns:
            Matrix[np.ndarray]: Matrix of probability for every class.
        """
        X_transformed = X.dot(self.rotation_matrix)
        return self.model.predict_proba(X_transformed)
