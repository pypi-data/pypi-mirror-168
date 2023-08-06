import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    """A custom sklearn transformer specifically for housing median price dataset

    This transformer creates new columns named rooms_per_household,
    population_per_household, and bedrooms_per_room (optional)

    Attributes
    ----------
    add_bedrooms_per_room : bool
        whether to add third feature bedrooms_per_room

    new_features : list
        list of names of new generated features

    Methods
    -------
    transform:
        transform input by generating new features
    """

    rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6

    def __init__(self, add_bedrooms_per_room=True):
        """Initialize the transformer

        Parameters
        ----------
        add_bedrooms_per_room : bool, optional
            whether to add third feature bedrooms_per_room, by default True
        """
        self.add_bedrooms_per_room = add_bedrooms_per_room

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """transform input by generating new features

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Input data, where `n_samples` is the number of samples and
            `n_features` is the number of features.

        Returns
        -------
        {ndarray, sparse matrix}
            `X` with new features
        """
        rooms_per_household = X[:, self.rooms_ix] / X[:, self.households_ix]
        population_per_household = X[:, self.population_ix] / X[:, self.households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, self.bedrooms_ix] / X[:, self.rooms_ix]
            self.new_features = [
                "rooms_per_household",
                "population_per_household",
                "bedrooms_per_room",
            ]
            return np.c_[
                X, rooms_per_household, population_per_household, bedrooms_per_room
            ]

        else:
            self.new_features = ["rooms_per_household", "population_per_household"]
            return np.c_[X, rooms_per_household, population_per_household]

    def get_feature_names(self):
        return self.new_features
