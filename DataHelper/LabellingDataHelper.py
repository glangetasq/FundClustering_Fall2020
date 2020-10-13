
import os
import numpy as np
import pandas as pd

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

    return df_year      # This is not standardized 


