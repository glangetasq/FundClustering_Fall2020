"""Create Fake Data"""

import datetime
import pandas as pd

class DataMaker:

    @staticmethod
    def make_fake_data(data_name=''):
        return DataMaker(label)


    def __init__(self, data_name=''):

        holding_asset_columns = ['crsp_fundno', 'caldt', 'cash', 'equity', 'bond', 'security']
        fund_mrnstar_columns = ['crsp_fundno', 'caldt', 'lipper_class_name']

        self.holding_asset = pd.DataFrame(columns=holding_asset_columns)
        self.holding_asset.caldt = pd.to_datetime(self.holding_asset.caldt, format='%Y%m%d')
        self.returns = pd.DataFrame()
        self.returns.index = pd.to_datetime(self.returns.index)
        self.fund_mrnstar = pd.DataFrame(columns=fund_mrnstar_columns)
        self.fund_mrnstar.caldt = pd.to_datetime(self.fund_mrnstar.caldt, format='%Y%m%d')
        self.fundno_ticker = pd.DataFrame()

        self.fake_data_name = data_name
        self.next_fund_id = 0



    def convert_to_data_cache(self, preprocessor, clustering_year):
        """
        Convert the data maker to a DataCache object for use in the model.

        Input:
            preprocessor : DataPreProcessor object
            clustering_year : int, year of interest.
        Output:
            DataCache object
        """
        return DataCache(self, preprocessor, clustering_year)


    def add_fake_fund(self, holding_asset_row, daily_returns_ts, fund_mrnstar_row):
        """
        Add a fund to the fake data.

        Input:
            holding_asset_row a dict with keys ['caldt', 'cash', 'equity', 'bond', 'security']
            daily_returns_ts a pd.Series of daily returns with day index in datetime
            fund_mrnstar a dict with keys ['caldt', 'lipper_class_name']
        Output:
            self : for Builder Design Pattern
        """

        # If caldt has been inputed as year, convert to datetime
        if isinstance(holding_asset_row.get('caldt'), int):
            date = datetime.datetime(year=holding_asset_row.get('caldt'), month=12, day=31) # HARD CODED VALUES
            holding_asset_row['caldt'] = date
        if isinstance(fund_mrnstar_row.get('caldt'), int):
            date = datetime.datetime(year=fund_mrnstar_row.get('caldt'), month=12, day=31) # HARD CODED VALUES
            fund_mrnstar_row['caldt'] = date

        # Check if correct format of input
        self.check_input_data(holding_asset_row, 'holding_asset')
        self.check_input_data(daily_returns_ts, 'returns')
        self.check_input_data(fund_mrnstar_row, 'fund_mrnstar')

        # Settle the fund_id in the data
        fund_id = self.next_fund_id
        holding_asset_row['crsp_fundno'] = fund_id
        fund_mrnstar_row['crsp_fundno'] = fund_id

        # Add data to the respective pd.DataFrame
        self.holding_asset = self.holding_asset.append(holding_asset_row, ignore_index=True)
        self.returns[fund_id] = daily_returns_ts
        self.fund_mrnstar = self.fund_mrnstar.append(fund_mrnstar_row, ignore_index=True)

        # ID must be unique. Increment for potential next fake fund.
        self.next_fund_id += 1

        return self


    def bulkadd_fake_fund(self, fake_data):
        """
        Bulk add fund data using add_fake_fund.

        Input:
            fake_data: list of 3-tuples (holding_asset_row, daily_returns_ts, fund_mrnstar)
        Output:
            None
        """

        for holding_asset_row, daily_returns_ts, fund_mrnstar in fake_data:
            self.add_fake_fund(holding_asset_row, daily_returns_ts, fund_mrnstar)




    def check_input_data(self, data, input_type):
        """
        Check if input is in the correct format.

        Return True if in the correct format, raise an error otherwise

        Input:
            data : input data
            input_type : str, type of input
        Output:
            test : bool
        """

        test = False

        if input_type == 'holding_asset':
            test = self._check_input_holding_asset_data(data)
        elif input_type == 'returns':
            test = self._check_input_returns_data(data)
        elif input_type == 'fund_mrnstar':
            test = self._check_input_fund_mrnstar_data(data)
        else:
            raise ValueError(f"{input_type} is not recognized as a valid input type")

        if not test:
            raise ValueError(f"{input_type} is not in a valid format for fund {self.next_fund_id}")

        return test


    def _check_input_holding_asset_data(self, holding_asset_row):
        return True


    def _check_input_returns_data(self, daily_returns_ts):
        return True


    def _check_input_fund_mrnstar_data(self, fund_mrnstar):
        return True


    def get_returns(self):
        return self.returns


    def get_holding_asset(self):
        return self.holding_asset


    def get_fund_mrnstar(self):
        return self.fund_mrnstar


    def get_fundno_ticker(self):
        return { i:i for i in self.returns.columns }
