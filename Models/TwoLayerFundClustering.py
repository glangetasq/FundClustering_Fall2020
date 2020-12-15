
# Local imports
from BaseClasses import MultipleLayerModelBased
from .HoldingDataMainClustering import HoldingDataMainClustering
from .DailyReturnsSubClustering import DailyReturnsSubClustering

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
        labels_first_layer = self.first_layer.fit()
        self.labels_first_layer = labels_first_layer

        # Second layer
        self.second_layer.set_up(labels_first_layer)
        labels_second_layer = self.second_layer.fit()
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

    def output_result(self, **kwargs):
        """Function to output the model, could use pickle to cached the obj that
        has been trained, so that you could load the obj later directly later, and you could also use this function
        to output the optimal portfolio, please use arguments to config what you want to output

        Parameters:
            output_model: bool
                output model to pickle container
            output_result_method:
                * if True : return results dataframe
                * if 'csv' : save results into csv files (one for each layer) and return results dataframe
                * if 'sql' : save results into sql table and return results dataframe
                * if None : do nothing
        """

        output_model = kwargs.get('output_model', False)
        output_result = kwargs.get('output_result', None)
        loc = kwargs.get('loc', None)

        if output_model == True:
            from Tools import save_model
            save_model.output_model(self, f'two_layer_model_{self.clustering_year}', loc)

        if output_result:

            from Tools import output_result
            first_layer_result = self.first_layer.output_result(
                output_cluster=True,
                save_result=False
            )
            output = output_result.output_result_two_layer(
                self.clustering_year,
                first_layer_result,
                self.labels_second_layer,
                self.labels_first_layer,
                save_result_method = output_result,
                loc = loc
            )


            return output
