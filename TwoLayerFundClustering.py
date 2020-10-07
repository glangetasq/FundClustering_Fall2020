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
        holding_asset_clustering = ('holding_asset_clustering', HoldingDataKMeanClustering()
        autoencoder_clustering = ('autoencoder_clustering', SecondLayerClustering())

        super().__init__([holding_asset_clustering, autoencoder_clustering], cached)

        self.clustering_year = clustering_year

    def remove_cache(self):
        """Remove the cached model parameters in the pipeline"""
        if self.cached:
            rmtree(self.cachedir)

    def fit(self, **kwargs):
        """Fit the pipeline based on the parameters
        Parameters:
            X: df/np.array/any customized type, but you need to make sure that all estimator could handle this data type
                independent variable, possibly you could use data_hlper class you define for this purpose
        """

        self.pipe[0].load_raw_data(self.clustering_year)
        self.pipe[1].load_raw_data()

        self.pipe[0].

        raise NotImplementedError("Subclasses should implement fit, expected to be something like could be something like return self.pipe.fit(X, Y)")

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
