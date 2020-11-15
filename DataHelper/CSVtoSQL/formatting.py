import numpy as np
import os
import pandas as pd

# Local Imports
from .morning_star_formatting_config import mrnstar_formatting_dict, mrnstar_new_name_dict

# Configuration
data_path = "/Users/glangetasq/Library/Mobile Documents/com~apple~CloudDocs/Columbia/Classes/Fall_20/DeepLearning/FundClusteringProject/DataSummer"

ticker_path = os.path.join(data_path, 'Tickers.csv')
returns_path = os.path.join(data_path, 'data_trimmed.csv')
morning_star_path = os.path.join(data_path, 'Summary_Updated.csv')


def ticker_formatting():

    ticker = pd.read_csv(ticker_path)
    columns = ['crsp_fundno', 'ticker']
    ticker = ticker[columns]
    ticker.columns = ['fundNo', 'fundTicker']
    ticker = ticker.drop_duplicates(subset=['fundNo'])

    return ticker


def returns_formatting():

    returns = pd.read_csv(returns_path, parse_dates=True)
    returns = pd.wide_to_long(returns, '', i='date', j='fundNo')
    returns.columns = ['r']

    return returns


def morning_star_formatting():

    mrnstar = pd.read_csv(morning_star_path)

    for colname in mrnstar:

        formatting_function = mrnstar_formatting_dict.get(colname, None)

        if formatting_function:
            mrnstar[colname] = formatting_function(mrnstar[colname])
        else:
            mrnstar = mrnstar.drop(colname, axis=1)

    mrnstar = mrnstar.rename(columns=mrnstar_new_name_dict)

    return mrnstar
