# Data Cache Class

class DataCache:
    """
    Cache the data needed for the model.

    Parameters:
        reader: an instance of the DataReader class
        processor: an instance of the DataProcessor class
        clustering_year: int, year of the clustering window

    TODO: clustering_year to clustering_period flexibility
    """

    def __init__(self, reader, preprocessor, clustering_year):

        if reader.is_reader_type('csv'):
            self._make_cache_from_csv_reader(reader, preprocessor, clustering_year)
        elif reader.is_reader_type('sql'):
            self._make_cache_from_sql_reader(reader, preprocessor, clustering_year)
        else:
            raise ValueError("This type of reader is not supported by DataCache at the moment.")


    def _make_cache_from_csv_reader(self, reader, preprocessor, clustering_year):

        # Daily returns of each mutual fund
        returns = reader.get_returns()
        self.returns = returns[returns.index.year == clustering_year]

        # Cumulative returns of each mutual fund
        self.cumul_returns = preprocessor.compute_cumulative_returns(self.returns)

        # Holding asset of each mutual fund
        holding_asset = reader.get_holding_asset()
        self.holding_asset = holding_asset[(holding_asset.caldt.dt.year == (clustering_year)) & (holding_asset.caldt.dt.month == 12)]
        self.asset_type = list(self.holding_asset.columns)[2:]

        # Morningstar category of each mutual fund
        fund_mrnstar = reader.get_fund_mrnstar()
        self.fund_mrnstar = fund_mrnstar[(fund_mrnstar.caldt.dt.year == (clustering_year)) & (fund_mrnstar.caldt.dt.month == 12)]

        # Fund number and ticker of each mutual fund
        self.fundno_ticker = reader.get_fundno_ticker()


    def _make_cache_from_sql_reader(self, reader, preprocessor, clustering_year):

            # Daily returns of each mutual fund
            lower_date = f"{clustering_year}-01-01"
            upper_date = f"{clustering_year}-12-31"
            self.returns = reader.get_returns(lower_date, upper_date)

            # Cumulative returns of each mutual fund
            self.cumul_returns = preprocessor.compute_cumulative_returns(self.returns)

            # Holding asset of each mutual fund
            self.holding_asset = reader.get_holding_asset(year=clustering_year, month=12)
            self.asset_type = list(self.holding_asset.columns)[2:]

            # Morningstar category of each mutual fund
            self.fund_mrnstar = reader.get_fund_mrnstar(year=clustering_year, month=12)

            # Fund number and ticker of each mutual fund
            self.fundno_ticker = reader.get_fundno_ticker()
