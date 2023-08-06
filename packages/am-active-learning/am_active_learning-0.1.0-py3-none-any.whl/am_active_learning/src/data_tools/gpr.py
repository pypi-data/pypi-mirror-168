#import gpflow
import numpy as np
from sklearn.model_selection import KFold
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from .property import Property

# def create_GPR(X, Y):
#     k = gpflow.kernels.RBF()
#     m = gpflow.models.GPR(data=(X, Y), kernel=k, mean_function=None)
#     opt = gpflow.optimizers.Scipy()
#     opt_logs = opt.minimize(m.training_loss, m.trainable_variables, options=dict(maxiter=100))
#     return m


def create_GPR_sk(X,Y, stdev = None):
    kernel = 1 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3))
    if stdev is not None:
        m = GaussianProcessRegressor(kernel=kernel, alpha = stdev,n_restarts_optimizer=9, normalize_y= True)
    else:
        m = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=9, normalize_y= True)

    m.fit(X, Y)
    return m

def train_GPR(X_tot, Y_tot, CV = True):
    if CV:
        kf = KFold(n_splits=10, shuffle = True)
        models = []
        error = []
        for train_index, test_index in kf.split(X_tot):
            X, xx = X_tot[train_index], X_tot[test_index]
            Y, yy = Y_tot[train_index], Y_tot[test_index]
            models.append(create_GPR(X, Y))
            m = models[-1]
            mean, var = m.predict_y(xx)
            error.append(OME(tf.cast(mean, tf.float32), yy))
            mean_train, var_train = m.predict_y(X)
        return models[error.index(min(error))]
    else:
        return create_GPR_sk(X_tot, Y_tot)

def model_building(data, x_var, y_var, dual_props = [],std = True):
    models = {}
    property_space = {}
    i = 0
    for prop in y_var:
        drop_rows = []
        data_temp = data.copy()
        for i in data.index:
            if not data_temp.loc[i, prop] >= 0:
                drop_rows.append(i)
        data_temp = data_temp.drop(drop_rows)
        Y_tot = np.array(data_temp[prop]).reshape(-1,1).astype(float)
        property_space[prop] = pd.DataFrame(data_temp[prop])
        if prop in dual_props:
            property_space["compressive " + prop] = pd.DataFrame(property_space[prop].loc[data_temp["type"] == 0])
            property_space["tensile " + prop] = pd.DataFrame(property_space[prop].loc[data_temp["type"] == 1])
            property_space["compressive " + prop].index.name = 'ID'
            property_space["tensile " + prop].index.name = 'ID'
        property_space[prop].index.name = 'ID'
        X_tot = np.array(data_temp.loc[:, x_var]).astype(float)
        if std:
            stdev = np.array(data_temp.loc[:, f'{prop}_stdev']).reshape(-1,).astype(float)
            models[prop] = create_GPR_sk(X_tot, Y_tot, stdev)
        else:
            models[prop] = create_GPR_sk(X_tot, Y_tot)
        i += 1
    return models, property_space

