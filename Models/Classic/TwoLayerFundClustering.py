
# Local imports
from BaseClasses import MultipleLayerModelBased
import DataHelper
from .HoldingDataMainClustering import HoldingDataMainClustering
from .DailyReturnsSubClustering import DailyReturnsSubClustering
import Tools


# Unknows imports.
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
        holding_asset_clustering = ('holding_asset_clustering', HoldingDataMainClustering())
        autoencoder_clustering = ('autoencoder_clustering', DailyReturnsSubClustering())

        # When trying to use the Pipeline, say error: models need to be Transformers?
        # super().__init__([], cached)

        self.first_layer = HoldingDataMainClustering()
        self.second_layer = DailyReturnsSubClustering()
        self.clustering_year = clustering_year

    def remove_cache(self):
        """Remove the cached model parameters in the pipeline"""
        if self.cached:
            rmtree(self.cachedir)


    def load_raw_data(self, catcher, **kwargs):
        """Function to load raw data from source, should be able to support reading data from flat file or sql database.
        Parameters:
            catcher: ClassicDataCatcher instance.
        """

        self.first_layer.load_raw_data(catcher=catcher, **kwargs)
        self.second_layer.load_raw_data(catcher=catcher, **kwargs)


    def fit(self, **kwargs):
        """Fit the pipeline based on the parameters
        Parameters:
            X: df/np.array/any customized type, but you need to make sure that all estimator could handle this data type
                independent variable, possibly you could use data_hlper class you define for this purpose
        """

        # First layer
        self.first_layer.set_up()
        labels_first_layer = self.first_layer.fit(**kwargs)
        self.labels_first_layer = labels_first_layer

        # Second layer
        self.second_layer.set_up(labels_first_layer)
        labels_second_layer = self.second_layer.fit(**kwargs)
        self.labels_second_layer = labels_second_layer

        return labels_second_layer

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

    def output_result(self, save_model=False, model_path=None, output_clustering_source=None, **kwargs):
        """Function to output the model, could use pickle to cached the obj that
        has been trained, so that you could load the obj later directly later, and you could also use this function
        to output the optimal portfolio, please use arguments to config what you want to output

        Parameters:
            save_model: bool
                save the model as a pickle to loc
            model_path: str
                path to save the model, raise Error if not defined and if save_model is True
            output_clustering_source: str
                source to which the cluster dataframe will be saved
        """

        Tools.save_model(save_model, path, self)

        if output_clustering_source:
            DataHelper.output_clustering_results(output_clustering_source, clusters, **kwargs)
