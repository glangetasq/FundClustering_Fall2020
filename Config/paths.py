import os

# PATHS

_DATA_PATH = "/Users/glangetasq/Library/Mobile Documents/com~apple~CloudDocs/Columbia/Classes/Fall_20/DeepLearning/FundClusteringProject/DataSummer"

DATA_PATHS = {
    'ticker' : os.path.join(_DATA_PATH, 'Tickers.csv'),
    'returns' : os.path.join(_DATA_PATH, 'data_trimmed.csv'),
    'morningstar' : os.path.join(_DATA_PATH, 'Summary_Updated.csv'),
    'holding_asset' : os.path.join(_DATA_PATH, 'Summary_Updated.csv'),
}
