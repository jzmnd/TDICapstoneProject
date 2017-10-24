#! /usr/bin/env python
"""
modellib.py
Model helper lib

Created by Jeremy Smith on 2017-10-17
j.smith.03@cantab.net
"""

from sklearn import base
from sklearn.model_selection import cross_val_score
import numpy as np


def compute_mse(est, X, y, k):
    """Calculates the MSE with k fold validation"""
    return -cross_val_score(est, X, y, cv=k, scoring='neg_mean_squared_error').mean()


class BaseResEnsembleEstimator(base.BaseEstimator, base.RegressorMixin):

    def __init__(self, base_est, resd_est):
        # Set base estimator and residual estimator
        self.base_est = base_est
        self.resd_est = resd_est

    def fit(self, X, y):
        # Fit base
        self.base_est.fit(X, y)
        # Calculate residual
        residual = y - self.base_est.predict(X)
        # Fit to residual
        self.resd_est.fit(X, residual)
        return self

    def predict(self, X):
        # Sum of base prediction and residual prediction
        return self.base_est.predict(X) + self.resd_est.predict(X)


class DataFrameSelector(base.BaseEstimator, base.TransformerMixin):

    def __init__(self, feature_names=None, dtype=np.int64, ntn=False):
        self.feature_names = feature_names
        self.dtype = dtype
        self.ntn = ntn

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.feature_names:
            Xarr = X[self.feature_names].as_matrix()
        else:
            Xarr = X.as_matrix()

        if self.ntn:
            Xarr = np.nan_to_num(Xarr)

        return Xarr.astype(self.dtype)


class EstimatorTransformer(base.BaseEstimator, base.TransformerMixin):

    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y):
        self.estimator.fit(X, y)
        return self

    def transform(self, X):
        p = self.estimator.predict(X)
        return p.reshape(-1, 1)


class ImputeNumber(base.BaseEstimator, base.TransformerMixin):
        
    def fit(self, X, y):
        return self
    
    def transform(self, X):
        return np.nan_to_num(X)
