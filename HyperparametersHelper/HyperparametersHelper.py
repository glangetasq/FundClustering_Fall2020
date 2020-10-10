# Helper to initialize and set hyperparameters
import argparse

def __make_parser():

    from config import DEFAULT_HYPERPARAMETERS

    parser = argparse.ArgumentParser(
        description='train',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Please implement in alphabetic order for clarity.
    # When implementing a new arg, make sure to add a default in the
    #  DEFAULT_HYPERPARAMETERS dictionary in config.
    parser.add_argument(
        '--ae_weights',
        default=DEFAULT_HYPERPARAMETERS['ae_weights'],
        help='pre-trained autoencoder weights'
    )
    parser.add_argument(
        '--alpha',
        default=DEFAULT_HYPERPARAMETERS['alpha'],
        type=float,
        help='coefficient in Student\'s kernel'
    )
    parser.add_argument(
        '--batch_size',
        default=DEFAULT_HYPERPARAMETERS['batch_size'],
        type=int
    )
    parser.add_argument(
        '--cluster_init',
        default=DEFAULT_HYPERPARAMETERS['cluster_init'],
        type=str,
        choices=['kmeans', 'hierarchical'],
        help='cluster initialization method'
    )
    parser.add_argument(
        '--dist_metric',
        default=DEFAULT_HYPERPARAMETERS['dist_metric'],
        type=str,
        choices=['eucl', 'cid', 'cor', 'acf'],
        help='distance metric between latent sequences'
    )
    parser.add_argument(
        '--epochs',
        default=DEFAULT_HYPERPARAMETERS['epochs'],
        type=int
    )
    parser.add_argument(
        '--eval_epochs',
        default=DEFAULT_HYPERPARAMETERS['eval_epochs'],
        type=int
    )
    parser.add_argument(
        '--gamma',
        default=DEFAULT_HYPERPARAMETERS['gamma'],
        type=float,
        help='coefficient of clustering loss'
    )
    parser.add_argument(
        '--kernel_size',
        default=DEFAULT_HYPERPARAMETERS['kernel_size'],
        type=int,
        help='size of kernel in convolutional layer'
    )
    parser.add_argument(
        '--n_clusters',
        default=DEFAULT_HYPERPARAMETERS['n_clusters'],
        type=int,
        help='number of clusters'
    )
    parser.add_argument(
        '--n_filters',
        default=DEFAULT_HYPERPARAMETERS['n_filters'],
        type=int,
        help='number of filters in convolutional layer'
    )
    parser.add_argument(
        '--n_units',
        nargs=2,
        default=DEFAULT_HYPERPARAMETERS['n_units'],
        type=int,
        help='numbers of units in the BiLSTM layers'
    )
    parser.add_argument(
        '--optimizer',
        default=DEFAULT_HYPERPARAMETERS['optimizer'],
        type=str
    )
    parser.add_argument(
        '--patience',
        default=DEFAULT_HYPERPARAMETERS['patience'],
        type=int,
        help='patience for stopping criterion'
    )
    parser.add_argument(
        '--pool_size',
        default=DEFAULT_HYPERPARAMETERS['pool_size'],
        type=int,
        help='pooling size in max pooling layer'
    ) #Encoder output will be (21, 2)
    parser.add_argument(
        '--pretrain_epochs',
        default=DEFAULT_HYPERPARAMETERS['pretrain_epochs'],
        type=int
    )
    parser.add_argument(
        '--pretrain_optimizer',
        default=DEFAULT_HYPERPARAMETERS['pretrain_optimizer'],
        type=str
    )
    parser.add_argument(
        '--save_dir',
        default=DEFAULT_HYPERPARAMETERS['save_dir']
    )
    parser.add_argument(
        '--save_epochs',
        default=DEFAULT_HYPERPARAMETERS['save_epochs'],
        type=int
    )
    parser.add_argument(
        '--strides',
        default=DEFAULT_HYPERPARAMETERS['strides'],
        type=int,
        help='strides in convolutional layer'
    )
    parser.add_argument(
        '--tol',
        default=DEFAULT_HYPERPARAMETERS['tol'],
        type=float,
        help='tolerance for stopping criterion'
    )
    parser.add_argument(
        '--validation',
        default=DEFAULT_HYPERPARAMETERS['validation'],
        type=bool,
        help='use train/validation split'
    )
    parser.add_argument(
        '--year',
        default=DEFAULT_HYPERPARAMETERS['year'],
        type=int
    )

    return parser


def parse_prm():
    parser = __make_parser()
    return parser.parse_args()


def create_prm(**kwargs):

    parser = __make_parser()
    args = parser.parse_args()

    for key, value in kwargs.items():

        if isinstance(value, str):
            exec(f"args.{key} = '{value}'")
        else:
            exec(f"args.{key} = {value}")

    return args
