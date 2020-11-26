import os

# PATHS

_DATA_PATH = "/Users/glangetasq/Library/Mobile Documents/com~apple~CloudDocs/Columbia/Classes/Fall_20/DeepLearning/FundClusteringProject/DataSummer"

PATHS = {
    'ticker' : os.path.join(_DATA_PATH, 'Tickers.csv'),
    'returns' : os.path.join(_DATA_PATH, 'data_trimmed.csv'),
    'morningstar' : os.path.join(_DATA_PATH, 'Summary_Updated.csv'),
    'holding_asset' : os.path.join(_DATA_PATH, 'Summary_Updated.csv'),
}

SQL_CONFIG = {
    'database' : 'fund_clustering',
    'tables' : {
        'ticker' : 'ticker',
        'returns' : 'returns',
        'morningstar' : 'morning_star',
        'holding_asset' : 'morning_star'
        },
    'default_login' : {
        'username' : 'fx_admin',
        'password' : '#Flexstone2020',
        'schema' : '',
        'secrets_dir' : '/Users/glangetas'}
}

# Hyperparameters

DEFAULT_HYPERPARAMETERS = {
    'ae_weights' : None,
    'alpha' : 1.0,
    'batch_size' : 64,
    'cluster_init' : 'hierarchical',
    'dist_metric' : 'eucl',
    'epochs' : 1000,
    'eval_epochs' : 20,
    'gamma' : 1.0,
    'kernel_size' : 10,
    'n_clusters' : None,
    'n_filters' : 50,
    'n_units' : [50, 1],
    'optimizer' : 'adam',
    'patience' : 5,
    'pool_size' : 12,
    'pretrain_epochs' : 500,
    'pretrain_optimizer' : 'adam',
    'save_dir' : 'result_secondlayer',
    'save_epochs' : 50,
    'strides' : 1,
    'tol' : 1e-3,
    'validation' : False,
    'year' : 2019,
}
