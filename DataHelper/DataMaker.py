"""Create Fake Data"""

import numpy as np
import pandas as pd
from .DataCatcher.BaseDataCatcher import BaseDataCatcher

class DataMaker(BaseDataCatcher):

    def __init__(self, data_name=''):

        super().__init__(reader=self)

        self.mrnstar = pd.DataFrame(
            index=[
                'fundNo',
                'date',
                'cash',
                'equity',
                'bond',
                'security',
                'lipper_class_name'
            ]
        )

        self.returns = pd.DataFrame()
        self.fundno_ticker = dict()

        self.fake_data_name = data_name
        self.next_fund_id = 0


    def add_fake_fund(self, mrnstar_row, returns_ts):
        """
        Add a fund to the fake data.

        Input:
            mrnstar_row: list with fundNo, date, cash, equity, bond, security, lipper_class_name
            returns_ts a pd.Series of daily returns with day index in datetime
        Output:
            self : for Builder Design Pattern
        """

        # Settle the fund_id in the data
        fund_id = self.next_fund_id

        self.returns[fund_id] = returns_ts
        self.mrnstar[fund_id] = mrnstar_row
        self.fundno_ticker[mrnstar_row[0]] = fund_id

        # ID must be unique. Increment for potential next fake fund.
        self.next_fund_id += 1

        return self


    def bulk_add_fake_fund(self, fake_data):
        """
        Bulk add fund data using add_fake_fund.

        Input:
            fake_data: list of 3-tuples (holding_asset_row, daily_returns_ts, fund_mrnstar)
        Output:
            None
        """

        for mrnstar_row, returns_ts in fake_data:
            self.add_fake_fund(mrnstar_row, returns_ts)


    def _pack_data(self):
        """
        Iterator that output the needed data for each layer
        """

        returns = self.returns.astype(np.float64)
        mrnstar = self.mrnstar.T
        mrnstar = mrnstar.astype(
            dtype = {
                'fundNo': int,
                'cash': np.float64,
                'equity': np.float64,
                'bond': np.float64,
                'security': np.float64,
                'lipper_class_name': str,
            }
        )
        mrnstar['date'] = pd.to_datetime(mrnstar['date'])

        _holding_asset_cols = ['cash', 'equity', 'bond', 'security']
        _fund_mrnstar_cols = ['fundNo', 'date', 'lipper_class_name']

        # First layer data
        yield {
            'features': mrnstar[_holding_asset_cols],
            'returns': returns,
            'cumul_returns': (1+returns).cumprod(),
            'asset_type': _holding_asset_cols,
            'fund_mrnstar': mrnstar[_fund_mrnstar_cols],
            'fundNo_ticker': self.fundno_ticker
        }

        # Second layer data
        yield {
            'features_first_layer': mrnstar[_holding_asset_cols],
            'returns': returns
        }
