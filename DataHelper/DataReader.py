
import pandas as pd

# Temporary path helper
# import Path
class Path:

    import os
    _data_path = "/Users/glangetasq/Library/Mobile Documents/com~apple~CloudDocs/Columbia/Classes/Fall_20/DeepLearning/FundClusteringProject/DataSummer"
    returns = os.path.join(_data_path, 'data_trimmed.csv')
    sp500 = os.path.join(_data_path, 'sp500.csv')
    tickers = os.path.join(_data_path, 'Tickers.csv')
    nameticker = os.path.join(_data_path, 'nameticker.xlsx')
    holding_asset = os.path.join(_data_path, 'Summary_Updated.csv')
    mrnstar = os.path.join(_data_path, 'Summary_Updated.csv')


class DataReader:

    def __init__(self):
        pass

    @staticmethod
    def get_returns():

        returns = pd.read_csv(Path.returns)
        returns = returns.set_index('date')
        returns.index = pd.to_datetime(returns.index)
        returns = returns.astype(float)

        return returns

    @staticmethod
    def get_holding_asset():

        holding_asset = pd.read_csv(Path.holding_asset)
        holding_asset = holding_asset.iloc[:, [0, 2]+[i for i in range(17, 30)]]
        holding_asset.caldt = pd.to_datetime(holding_asset.caldt, format='%Y%m%d')

        # TODO: separate the reading and preprocessing
        holding_asset['per_equity'] = holding_asset['per_com'] + holding_asset['per_pref'] + holding_asset['per_eq_oth']
        holding_asset['per_bond'] = holding_asset['per_conv'] + holding_asset['per_corp'] + holding_asset['per_muni'] + holding_asset['per_govt']
        holding_asset['per_sec'] = holding_asset['per_abs'] + holding_asset['per_mbs'] + holding_asset['per_fi_oth'] + holding_asset['per_oth']

        holding_asset = holding_asset[['crsp_fundno', 'caldt', 'per_cash', 'per_equity', 'per_bond', 'per_sec']]
        holding_asset.columns = ['crsp_fundno', 'caldt', 'cash', 'equity', 'bond', 'security']

        return holding_asset


    @staticmethod
    def get_fund_mrnstar():

        fund_mrnstar = pd.read_csv(Path.mrnstar)
        fund_mrnstar = fund_mrnstar[['crsp_fundno', 'caldt', 'lipper_class_name']]
        fund_mrnstar.caldt = pd.to_datetime(fund_mrnstar.caldt, format='%Y%m%d')

        return fund_mrnstar
   

    @staticmethod
    def get_fundno_ticker():

        ticker_data = pd.read_csv(Path.tickers)
        fundno_ticker = {}
        for i in range(ticker_data.shape[0]):
            if pd.isnull(ticker_data.ticker[i]):
                continue
            fundno_ticker[ticker_data.crsp_fundno[i]] = ticker_data.ticker[i]

        return fundno_ticker
