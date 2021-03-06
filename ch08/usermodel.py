# This code is supporting material for the book
# Building Machine Learning Systems with Python
# by Willi Richert and Luis Pedro Coelho
# published by PACKT Publishing
#
# It is made available under the MIT License

import numpy as np
from sklearn.linear_model import LassoCV, RidgeCV, ElasticNetCV
from sklearn.model_selection import KFold
from .load_ml100k import load


def learn_for(reviews, i):
    reg = ElasticNetCV(fit_intercept=True, alphas=[
                       0.0125, 0.025, 0.05, .125, .25, .5, 1., 2., 4.])
    u = reviews[i]
    us = range(reviews.shape[0])
    us = np.delete(us, i)
    ps, = np.where(u.toarray().ravel() > 0) 
    x = reviews[us][:, ps].T
    y = u.data
    kf = KFold(n_splits=4)
    predictions = np.zeros(len(u.toarray().ravel())) # 他のモデルと形を合わせるため，評価が行われていない映画はpredictionsを0にする
    for train, test in kf.split(y):
        xc = x[train].copy().toarray()
        x1 = np.array([xi[xi > 0].mean() for xi in xc])
        x1 = np.nan_to_num(x1)

        for i in range(xc.shape[0]):
            xc[i] -= (xc[i] > 0) * x1[i]

        reg.fit(xc, y[train] - x1)

        xc = x[test].copy().toarray()
        x1 = np.array([xi[xi > 0].mean() for xi in xc])
        x1 = np.nan_to_num(x1)

        for i in range(xc.shape[0]):
            xc[i] -= (xc[i] > 0) * x1[i]

        p = np.array(reg.predict(xc)).ravel()
        predictions[test] = p
    return predictions


def all_estimates(reviews):
    whole_data = []
    for i in range(reviews.shape[0]):
        s = learn_for(reviews, i)
        whole_data.append(s)
    return np.array(whole_data)
