""" Get scaled return and/or cumulative return time series data and fund numbers """

import numpy as np
from sklearn import preprocessing

def get_timeseries(ret_flag=False, val_flag=False, ret_data=None, feature=None, label=None, group=None):
    """
    ret: the daily return time series data of each fund
    val: the cumulative return time series data of each fund
    ret and val should at least provide one
    year: the clustering year, should be consistent with the first layer
    label: the clustering result from the first layer
    group: the specific group in the label to sub-cluster on
    feature: the feature data used in the first layer, to help match the fund number with the label
    """
        
    if ret_flag and val_flag:
        ret = ret_data
        ret = ret[feature.index]
        ret = ret.iloc[:, label==group]
        val = (ret+1).cumprod()
        fundnos = ret.columns
        ret_train = ret.T
        val_train = val.T
        scaler1 = preprocessing.StandardScaler()
        scaler2 = preprocessing.StandardScaler()
        ret_train = scaler1.fit_transform(ret_train)
        val_train = scaler2.fit_transform(val_train)

        #reshape
        array1 = np.array(ret_train).reshape([ret_train.shape[0], ret_train.shape[1], -1])
        array2 = np.array(val_train).reshape([val_train.shape[0], val_train.shape[1], -1])
        res_train = np.concatenate((array1, array2), axis = 2)
        
        return res_train, fundnos

    elif ret_flag or val_flag:
        df = ret_data
        df = df[feature.index]
        df = df.iloc[:, label==group]
        if ret:
            pass
        else:
            df = (df+1).cumprod()
        fundnos = df.columns
        df_train = df.T
        scaler1 = preprocessing.StandardScaler()
        df_train = scaler1.fit_transform(df_train)

        #reshape
        res_train = np.array(df_train).reshape([df_train.shape[0], df_train.shape[1], -1])
        
        return res_train, fundnos

    else:
        raise ValueError('Should at least provide one')