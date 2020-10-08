import numpy as np
import pandas as pd

class DataProcessor:
    """
    Class helping to process the data for the models
    """

    def __init__(self):
        pass

    @staticmethod
    def holding_asset_pivot(data_cache):
        """
        Features for first layer clustering.

        TODO: Not sure what this function do at the moment... Does that only pivot the holding_asset data frame?
        """

        features = pd.DataFrame( index = data_cache.returns.columns )
        funds = set(data_cache.holding_asset.crsp_fundno.values)

        for index in features.index:
            if int(index) in funds:
                for a in data_cache.asset_type:
                    features.loc[index, a] = data_cache.holding_asset[data_cache.holding_asset.crsp_fundno == int(index)][a].values[0]
            else:
                for a in data_cache.asset_type:
                    features.loc[index, a] = np.NaN

        features.dropna(axis=0, inplace=True)

        return features
