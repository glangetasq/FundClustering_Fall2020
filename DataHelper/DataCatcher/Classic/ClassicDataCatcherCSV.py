
import pandas as pd

# Local imports
import Config
import DataHelper
from ..BaseCSVDataCatcher import BaseCSVDataCatcher
from Tools.latest_date_in_dataframe import latest_date_in_dataframe

class ClassicDataCatcherCSV(BaseCSVDataCatcher):

    __instance = None

    DATA_NEEDS = {
        'returns' : ('fund_clustering', 'returns'),
        'ticker' : ('fund_clustering', 'ticker'),
        'morning_star' : ('fund_clustering', 'morning_star'),
    }

    def __init__(self):
        raise RuntimeError('Call instance() instead')


    @classmethod
    def instance(cls, **kwargs):

        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            super(cls, cls.__instance).__init__(**kwargs)

        return cls.__instance



    def process(self, verbose=True, n_funds=None):

        super().load_data(verbose)

        if verbose:
            print("Processing data...")


        # Returns processing
        db_name, table_name = self.DATA_NEEDS['returns']
        returns = self.reader.get_dataframe(db_name, table_name)
        returns['date'] = pd.to_datetime(returns['date'])
        # Only take date between TMIN and TMAX
        returns = returns.set_index('date')
        returns = returns[Config.TMIN <= returns.index]
        returns = returns[returns.index <= Config.TMAX]
        # Set columns to int, so it can be merged later with morningstar
        returns.columns = returns.columns.astype(int)

        # Holding Asset and Morningstar processing
        db_name, table_name = self.DATA_NEEDS['morning_star']
        morning_star = self.reader.get_dataframe(db_name, table_name)
        # Rename and formatting
        morning_star = morning_star.rename(columns={'crsp_fundno':'fundNo', 'caldt':'date'})
        morning_star['date'] = pd.to_datetime(morning_star['date'], format='%Y%m%d')
        # Create the features for first_layer (equity, sec, cash and bond)
        tmp = [
            ('cash', ['per_cash']),
            ('bond', ['per_govt', 'per_muni', 'per_conv', 'per_corp']),
            ('equity', ['per_com', 'per_pref', 'per_eq_oth']),
            ('security', ['per_abs', 'per_mbs', 'per_fi_oth', 'per_oth']),
        ]
        for new_col, col2sum in tmp:
            morning_star[new_col] = morning_star[col2sum].sum(axis=1)
        # Take only last date of morning_star data
        morning_star = morning_star.groupby('fundNo').apply(latest_date_in_dataframe('date'))
        #morning_star.index = morning_star.index.astype(int)

        # Merge returns and morningstar fundNo
        merged_funds = list(set(returns.columns).intersection(morning_star.index))
        if n_funds: merged_funds = merged_funds[:n_funds]
        morning_star = morning_star.loc[merged_funds]
        returns = returns[merged_funds]

        # Ticker processing
        db_name, table_name = self.DATA_NEEDS['ticker']
        ticker = self.reader.get_dataframe(db_name, table_name)
        # Rename and formatting
        ticker = ticker.rename(columns={'crsp_fundno':'fundNo', 'caldt':'date'})
        ticker['date'] = pd.to_datetime(ticker['date'], format='%Y%m%d')
        # Only takes date between TMIN and TMAX
        ticker = ticker[Config.TMIN <= ticker['date']]
        ticker = ticker[ticker['date'] <= Config.TMAX]
        # Keep only last date
        ticker = ticker.groupby('fundNo').apply(latest_date_in_dataframe('date'))
        ticker = ticker.set_index('fundNo')['ticker'].to_dict()

        if verbose: print("... Finished processing data")

        # Save dataframes to self
        self.returns = returns
        self.morning_star = morning_star
        self.ticker = ticker


    def _pack_data(self):
        """
        Iterator that output the needed data for each layer
        """

        _holding_asset_cols = ['cash', 'equity', 'bond', 'security']
        _fund_mrnstar_cols = ['fundNo', 'date', 'lipper_class_name']
        layers = list()

        # First layer data
        layers.append({
            'features': self.morning_star[_holding_asset_cols],
            'returns': self.returns,
            'cumul_returns': (1+self.returns).cumprod(),
            'asset_type': _holding_asset_cols,
            'fund_mrnstar': self.morning_star[_fund_mrnstar_cols],
            'fundNo_ticker': self.ticker
        })

        # Second layer data
        layers.append({
            'features_first_layer': self.morning_star[_holding_asset_cols],
            'returns': self.returns
        })

        for layer_data in layers:
            yield layer_data
