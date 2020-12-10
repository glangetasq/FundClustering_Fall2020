

# Local imports
from ..BaseSQLDataCatcher import BaseSQLDataCatcher
from Tools.latest_date_in_dataframe import latest_date_in_dataframe

class ClassicDataCatcherSQL(BaseSQLDataCatcher):

    __instance = None

    DATA_NEEDS = {
        'returns' : ('fund_clustering', 'returns'),
        'ticker' : ('fund_clustering', 'ticker'),
        'morning_star' : ('fund_clustering', 'morning_star'),
    ]

    def __init__(self):
        raise RuntimeError('Call instance() instead')


    @classmethod
    def instance(cls, **kwargs):

        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            super(cls, cls.__instance).__init__(**kwargs)

        return cls.__instance


    def process(self, verbose=True):

        super().load_data(verbose)

        if verbose:
            print("Processing data...")


        # Returns processing
        db_name, table_name = self.DATA_NEEDS['returns']
        returns = self.reader.get_dataframe(db_name, table_name)
        returns = returns.pivot(index='date', columns='fundNo', values='r')
        returns.index = pd.to_datetime(returns.index)

        # Holding Asset and Morningstar processing
        db_name, table_name = self.DATA_NEEDS['morning_star']
        morning_star = self.reader.get_dataframe(db_name, table_name)
        # Take only the latest data for each fund
        morning_star = morning_star.groupby('fundNo').apply(latest_date_in_dataframe)

        # Ticker processing
        db_name, table_name = self.DATA_NEEDS['ticker']
        ticker = self.reader.get_dataframe(db_name, table_name)
        ticker = ticker.set_index('fundNo')['ticker'].to_dict()
