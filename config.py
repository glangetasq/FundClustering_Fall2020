# Configuration of the models


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
