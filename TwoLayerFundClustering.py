from BaseClasses import MultipleLayerModelBased
from HoldingDataClustering import HoldingDataKMeanClustering
from SecondLayerClustering import SecondLayerClustering

rmtree = lambda : None # from shutil import rmtree
mkdtemp = lambda : None# from tempfile import mkdtemp

class TwoLayerFundClustering(MultipleLayerModelBased):
    """Handle the logistics of the pipeline of the two layer fund clustering.
    Handle the set up, fit and predict of the pipeline made of
    HoldingDataClustering (Iterative KMean) and SecondLayerClustering (autoencoder)
    """

    def __init__(self, clustering_year, cached = False):
        """
        Set up the pipeline for the multiple layer that we use in the model construction

        Parameters:

        estimators: list of turple
            example: [('reduce_dim', pca2), ('clf', svm2)] this would be a list of ('model_name', estimator), the estimator could be
            a customized class inherit from BaseEstimator, based on the model you have, the estimator could be transformer or estimator,
            and based on the machine model, estimator could be classifer or regressor, check the next class defintion for more detail
        """
        holding_asset_clustering = ('holding_asset_clustering', HoldingDataKMeanClustering())
        autoencoder_clustering = ('autoencoder_clustering', SecondLayerClustering())

        # When trying to use the Pipeline, say error: models need to be Transformers?
        #super().__init__([], cached)

        self.first_layer = HoldingDataKMeanClustering()
        self.second_layer = SecondLayerClustering()
        self.clustering_year = clustering_year

    def remove_cache(self):
        """Remove the cached model parameters in the pipeline"""
        if self.cached:
            rmtree(self.cachedir)


    def args(self):
        import argparse
        parser = argparse.ArgumentParser(description='train', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # parser.add_argument('--dataset', default='CBF', help='UCR/UEA univariate or multivariate dataset')
        #parser.add_argument('--validation', default=False, type=bool, help='use train/validation split')
        parser.add_argument('--year', default=2019, type=int)
        parser.add_argument('--ae_weights', default=None, help='pre-trained autoencoder weights')
        parser.add_argument('--n_clusters', default=None, type=int, help='number of clusters')
        parser.add_argument('--n_filters', default=50, type=int, help='number of filters in convolutional layer')
        parser.add_argument('--kernel_size', default=10, type=int, help='size of kernel in convolutional layer')
        parser.add_argument('--strides', default=1, type=int, help='strides in convolutional layer')
        parser.add_argument('--pool_size', default=12, type=int, help='pooling size in max pooling layer') #Encoder output will be (21, 2)
        parser.add_argument('--n_units', nargs=2, default=[50, 1], type=int, help='numbers of units in the BiLSTM layers')
        parser.add_argument('--gamma', default=1.0, type=float, help='coefficient of clustering loss')
        parser.add_argument('--alpha', default=1.0, type=float, help='coefficient in Student\'s kernel')
        parser.add_argument('--dist_metric', default='eucl', type=str, choices=['eucl', 'cid', 'cor', 'acf'], help='distance metric between latent sequences')
        parser.add_argument('--cluster_init', default='hierarchical', type=str, choices=['kmeans', 'hierarchical'], help='cluster initialization method')
        parser.add_argument('--pretrain_epochs', default=500, type=int)
        parser.add_argument('--pretrain_optimizer', default='adam', type=str)
        parser.add_argument('--epochs', default=1000, type=int)
        parser.add_argument('--optimizer', default='adam', type=str)
        parser.add_argument('--eval_epochs', default=20, type=int)
        parser.add_argument('--save_epochs', default=50, type=int)
        parser.add_argument('--batch_size', default=64, type=int)
        parser.add_argument('--tol', default=0.001, type=float, help='tolerance for stopping criterion')
        parser.add_argument('--patience', default=5, type=int, help='patience for stopping criterion')
        parser.add_argument('--save_dir', default='result_secondlayer')
        args = parser.parse_args(args=[])

        return args


    def fit(self, **kwargs):
        """Fit the pipeline based on the parameters
        Parameters:
            X: df/np.array/any customized type, but you need to make sure that all estimator could handle this data type
                independent variable, possibly you could use data_hlper class you define for this purpose
        """

        # First layer
        self.first_layer.load_raw_data(self.clustering_year)
        self.first_layer.set_up()
        first_layer_labels = self.first_layer.fit()

        # Second layer for each group
        features_first_layer = self.first_layer.features
        cluster_subcluster_dict = dict()
        args = self.args()
        self.second_layer.load_raw_data(self.clustering_year, first_layer_labels)

        for main_cluster in range(len(set(first_layer_labels))):

            self.second_layer.set_up(features_first_layer, first_layer_labels, main_cluster)
            second_layer_result = self.second_layer.fit(args)

            for fund_no, sub_cluster in second_layer_result:
                cluster_subcluster_dict[fund_no] = (main_cluster, sub_cluster)


        return cluster_subcluster_dict


    def predict(self, **kwargs):
        """Run prediction after fitting the model, should throw error message when the model did not run fit yet.

        Parameters:
            X: df/np.array/any customized type, but you need to make sure that all estimator could handle this data type
                independent variable
            Y: df/np.array/any customized type, but you need to make sure that all estimator could handle this data type
                dependent variable, if it is just a unsupervised problem, you may not have Y
        """
        raise NotImplementedError("Subclasses should implement predict")

    def model_summary(self):
        """Function that provide summary of model result: prediction accuracy, different matrix
            to measure the model, and hyper-parameters of the model"

        Parameters:
            None

            Return
                dict {str: float/dataframe}
                key is the staticial measure name
                value is the statical measure, either a number or a matrix or a dataframe
        """
        raise NotImplementedError("Subclasses should implement model_summary")

    def output_result(self, **kwargs):
        """Function to output the model, could use pickle to cached the obj that
        has been trained, so that you could load the obj later directly later, and you could also use this function
        to output the optimal portfolio, please use arguments to config what you want to output

        Parameters:
            output_model: bool
                output model to pickle container
            output_portfolio: bool
                output optimal portfolio generated
        """
        raise NotImplementedError("Subclasses should implement output_result")
