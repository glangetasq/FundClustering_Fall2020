""" Implementation of second layer clustering by return data """

# Local imports
from BaseClasses import FundClusterBased
import HyperparametersHelper
from .OneMainClusterDailyReturnsSubClustering import OneMainClusterDailyReturnsSubClustering


class DailyReturnsSubClustering(FundClusterBased):

    """Clustering algorithm to define the cluster of a specific clustering method used to define cateogry of mutual fund"""
    def __init__(self):

        super().__init__("Daily Returns Sub Clustering")
        self._one_main_cluster_subclustering = OneMainClusterDailyReturnsSubClustering()
        self.hasBeenFit = False

    def set_up(self, first_layer_labels, **kwargs):
        """Function to setup any private variable for the allocator"""

        self._first_layer_labels = first_layer_labels
        self._set_up_kwargs = kwargs


    def cluster_method(self):
        """This provide identifier of the clustering strategy that you are implementing."""
        return self._cluster_method_name


    def machine_learning_based(self):
        """This method tells us whether the cluster category is machine learning
            based and need to run fit to train model parameters or not
        Parameters:
            None
            Return
                bool
                True if the strategy need to run fit to be ready for prediction, otherwise No
        """
        return self.hasBeenFit


    def load_raw_data(self, catcher, **kwargs):
        """Function to load raw data from source, should be able to support
        reading data from flat file or sql database. Please just implement the one using flat file now,
        later we would provide the sql python package that we would want to utilize for the database task

        Load data for every sub-clustering instance.
        """

        _DATA_NEEDS = [
            'features_first_layer',
            'returns',
        ]

        feat_fl, ret = catcher.unpack_data(keys=_DATA_NEEDS)

        self._features_first_layer = feat_fl
        self._returns = ret

        self.clustering_year = Config.CLUSTERING_YEAR



    def set_hyper_parameter(self, **kwargs):
        """Function to re_config any hyper parameters that you need for your model,
        the parameters should be initialized in your inherited setup function, by reading the config
        either from a config file or from argument, but please enable user to have a config file to set
        these hyper-parameters."""
        raise NotImplementedError("Subclasses should implement set_hyper_parameter!")


    def print_hyper_parameter(self, **kwargs):
        """Print all the hyper parameters that you set for your model."""
        raise NotImplementedError("Subclasses should implement print_hyper_parameter!")


    def fit(self, hyper_parameters=HyperparametersHelper.default_prm(), **kwargs):
        """Function to execute training either based on the data that you load from file or passed in as argument.
        When X, Y are passed in as argument, would train the model based on the training dataset passed in, and over write
        the existing data cached in the strategy obj. If you implement some new machine learning model rather than using
        existing machine learning model by some python package, please seperate the implementation of the model in another class,
        and initialize an instance of that model in your setup function rather than implement the model directly in the fit function,
        so that we could seprate the business logics with the machine learning model maintaining logics, and those model could be reused
        somewhere else too.
        TODO: Could modularize even more this function.
        """

        cluster_subcluster_dict = dict()

        for main_cluster in range(len(set(self._first_layer_labels))):

            self._one_main_cluster_subclustering.set_up(
                self._features_first_layer,
                self._first_layer_labels,
                self._returns,
                main_cluster,
                **self._set_up_kwargs
            )

            second_layer_result = self._one_main_cluster_subclustering.fit(hyper_parameters)


            for fund_no, sub_cluster in second_layer_result.items():
                cluster_subcluster_dict[fund_no] = (main_cluster, sub_cluster)

        self.hasBeenFit = True
        self.cluster_subcluster_dict = cluster_subcluster_dict

        return cluster_subcluster_dict


    def predict(self, **kwargs):
        """Run prediction after fitting the model, should throw error message when the model did not run fit yet."""
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
        to output the optimal cluster, please use arguments to config what you want to output
        Parameters:
            output_model: bool
                output model to pickle container
            output_cluster: bool
                output cluster for each fund
        """

        if self.hasBeenFit == False:
            print('Please fit the model!')
            return 0

        output_model = kwargs.get('output_model', False)
        output_cluster = kwargs.get('output_cluster', False)
        loc = kwargs.get('loc', None)
        save_result = kwargs.get('save_result', True)

        if output_model == True:
            from Tools import save_model
            save_model.output_model(self, f'second_layer_model_{self.clustering_year}', loc)

        if output_cluster == True:
            from Tools import output_result
            output = output_result.output_result_secondlayer(self.clustering_year, self.cluster_subcluster_dict,
                                                             save_result, loc)
            return output
