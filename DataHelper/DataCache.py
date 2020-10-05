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

        final_month = 12 # TODO: not sure what filtering by December means in the code below

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
