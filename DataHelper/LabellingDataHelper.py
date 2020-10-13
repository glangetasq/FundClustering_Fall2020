
import os
import numpy as np
import pandas as pd
from Tools import get_features

data_path = "~/Desktop/Columbia/E4742 Deep Learning/FundClustering_Fall2020/Summer20Project/Final delivery/Clustering Model/Data"
 

def LabellingDataHelper(year):

    asset = pd.read_csv(data_path+"/Summary_Updated.csv")
    df = asset[asset['summary_period2']=='AQ'] #only picking out annual data
    df['caldt'] = pd.to_datetime(df['caldt'], format='%Y%m%d')
    df['year'] = pd.DatetimeIndex(df['caldt']).year
    df = df[['crsp_fundno','year','per_com', 'per_pref', 'per_conv', 'per_corp', 'per_muni', 'per_govt','per_oth', 'per_cash', 'per_abs', 'per_mbs', 'per_eq_oth','per_fi_oth']].astype('float64')
    df.columns = ['crsp_fundno','year','Common Stock', 'Preferred Stock', 'Convertible Bonds', 
                    'Corporate Bonds', 'Muni Bonds', 'Gov Bonds','Other Securities', 'Cash', 'ABS', 
                    'MBS', 'Other Equity','Other FI']

    temp = df.drop(['year','crsp_fundno'],axis=1)
    df = df.loc[(temp.sum(axis=1) <= 150) & (temp.sum(axis=1) >= 75)]

    # pulling in daily returns data over the years
    data_trimmed = pd.read_csv(data_path+'/data_trimmed.csv').set_index('date')
    data_trimmed.index = pd.to_datetime(data_trimmed.index)
    data_trimmed = data_trimmed.astype(float)   

    data = data_trimmed[data_trimmed.index.year == year]

    # Cumulative annual return
    value = (data+1).cumprod() 

    # Finding the overlap between the mutual funds included in CRSP data and returns data. 
    # (I think some are missing.)
    overlap = list(set(value.columns.astype(int)).intersection(set(df['crsp_fundno'])))
    df = df[df['crsp_fundno'].isin(overlap)]
    df.set_index('crsp_fundno',drop=True)
    df.dropna(axis=0, inplace=True)

    # Filtering for a specific year's data 
    df_year = df[df['year']==year]
    df_year.drop('year',axis=1,inplace=True)
    df_year.dropna(axis=0, inplace=True)

    ### Feature generation
    sp500 = pd.read_csv(data_path+'/sp500.csv')
    sp500.date = pd.to_datetime(sp500.date)
    market = sp500['return'][sp500.date.dt.year==year]
    
    features = pd.DataFrame(index=data.columns)
    features['annual_ret'] = ((data+1).prod(axis=0)-1)
    features['pos_days'] = (data>0).sum(axis=0)
    features['zero_days'] = (data==0).sum(axis=0)
    features['vol'] = data.std(axis=0)
    features['max_dd'] = data.apply(lambda x:get_features.maxdd(x), axis = 0)
    features['beta'] = data.apply(lambda x:get_features.beta(x,market), axis = 0)   

    return df, df_year, features      # This is not standardized 


