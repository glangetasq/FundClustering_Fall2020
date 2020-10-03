# Data Helper

import Path
import pandas as pd

class DataHelper:

    def get_returns(clustering_year):

        returns = pd.read_csv(Path.returns)

        return returns[returns.index.year == clustering_year]


    def get_cumul_returns(clustering_year):

        returns = DataHelper.get_returns(clustering_year)

        return (1+returns).cumprod()


    def get_holding_asset(clustering_year, month=12):

        holding_asset = pd.read_csv(Path.holding_asset)
        holding_asset = holding_asset.iloc[:, [0, 2]+[i for i in range(17, 30)]]

        # Data Processing

        holding_asset['per_equity'] = holding_asset['per_com'] + holding_asset['per_pref'] + holding_asset['per_eq_oth']
        holding_asset['per_bond'] = holding_asset['per_conv'] + holding_asset['per_corp'] + holding_asset['per_muni'] + holding_asset['per_govt']
        holding_asset['per_sec'] = holding_asset['per_abs'] + holding_asset['per_mbs'] + holding_asset['per_fi_oth'] + holding_asset['per_oth']
        holding_asset.caldt = pd.to_datetime(holding_asset.caldt, format='%Y%m%d')
        holding_asset = holding_asset[['crsp_fundno', 'caldt', 'per_cash', 'per_equity', 'per_bond', 'per_sec']]
        holding_asset.columns = ['crsp_fundno', 'caldt', 'cash', 'equity', 'bond', 'security']

        return holding_asset[(holding_asset.caldt.dt.year == clustering_year) & (holding_asset.caldt.dt.month == month)]


    def get_mrnstar_class(clustering_year, month=12):

        fund_mrnstar = pd.read_csv(Path.mrnstar)

        fund_mrnstar = fund_mrnstar[['crsp_fundno', 'caldt', 'lipper_class_name']]
        fund_mrnstar.caldt = pd.to_datetime(fnd_mornstar.caldt, format='%Y%m%d')

        return fund_mrnstar[(fund_mrnstar.caldt.dt.year == (clustering_year)) & (fund_mrnstar.caldt.dt.month == 12)]
