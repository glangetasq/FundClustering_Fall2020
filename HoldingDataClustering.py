""" Implementation of clustering by holding data only """

from BaseClasses import FundClusterBased
from DataHelper import *
import Tools

import numpy as np
import pandas as pd
from sklearn import cluster as sklearn_cluster

class HoldingDataKMeanClustering(FundClusterBased):

    """Clustering algorithm to define the cluster of a specific clustering method used to define cateogry of mutual fund"""
    def __init__(self):

        super().__init__("HoldgingData_KMean_Clustering")

        self.hadBeenFit = False

    def set_up(self, **kwargs):
        """Function to setup any private variable for the allocator"""

        self.asset_type = list(self.data.holding_asset.columns)[2:]
        self.label = None
        self.k = None

    @property
    def normalized_features(self):

        norm_features = Tools.normal_standardization(self.features)
        norm_features = np.round(norm_features, 4)

        return norm_features

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

    def load_raw_data(self, clustering_year, source_type='DataHelper', **kwargs):
        """Function to load raw data from source, should be able to support
        reading data from flat file or sql database. Please just implement the one using flat file now,
        later we would provide the sql python package that we would want to utilize for the database task

        Parameters:
            clustering_year: int
                year of data
                TODO: change the parameter so it allow custom clustering windows
            source_type: str
                flat file type or sql, if it is flat file, file directory or
                path need to be passed in as argument or in the setup function
                If it is sql, connection need to be extablished in setup function
                please avoid any hard coded name in the class, and set global variable to define those file name
        """

        if source_type == 'DataHelper':
            self.data = DataHelper.get_data_cache(clustering_year)

            # Processing data for this model
            processor = DataHelper.get_data_processor()
            self.features = processor.holding_asset_pivot(self.data)
        else:
            raise ValueError(f"The type of source '{source_type}' is not supported at the moment.")


    def set_hyper_parameter(self, **kwargs):
        """Function to re_config any hyper parameters that you need for your model,
        the parameters should be initialized in your inherited setup function, by reading the config
        either from a config file or from argument, but please enable user to have a config file to set
        these hyper-parameters."""
        raise NotImplementedError("Subclasses should implement set_hyper_parameter!")

    def print_hyper_parameter(self, **kwargs):
        """Print all the hyper parameters that you set for your model."""
        raise NotImplementedError("Subclasses should implement print_hyper_parameter!")

    def fit(self, **kwargs):
        """Function to execute training either based on the data that you load from file or passed in as argument.
        When X, Y are passed in as argument, would train the model based on the training dataset passed in, and over write
        the existing data cached in the strategy obj. If you implement some new machine learning model rather than using
        existing machine learning model by some python package, please seperate the implementation of the model in another class,
        and initialize an instance of that model in your setup function rather than implement the model directly in the fit function,
        so that we could seprate the business logics with the machine learning model maintaining logics, and those model could be reused
        somewhere else too.

        Kwargs:
            X : data as a DataCache instance. If not given, load_raw_data needs to be called beforehand.

        TODO: Could modularize even more this function.
        """

        # kwargs
        log = kwargs.get('log', None)
        verbose = kwargs.get('verbose', True)
        identical_asset = kwargs.get('identical_asset', 3)
        argsort = kwargs.get('argsort', False)

        # features
        if 'X' in kwargs:
            features = kwargs.get('X')
            normalized_features = Tools.normal_standardization(self.features)
            normalized_features = np.round(normalized_features, 4)
        else:
            # TODO: error if load_raw_data has not been called before
            features = self.features
            #normalized_features = self.normalized_features
            normalized_features = Tools.normal_standardization(features)
            normalized_features = np.round(normalized_features, 4)

        k = Tools.silhouette(normalized_features, log)
        h_clustering = sklearn_cluster.AgglomerativeClustering(n_clusters=k, linkage='ward').fit(normalized_features)
        cluster_label = h_clustering.labels_
        if verbose: print('Best number of clusters for hierarchical clustering is', k)

        #Screen out the outliers
        length1 = -1
        length2 = -2
        if verbose: print('Starting searching and grouping outliers')
        #Look for the outliers
        while length1 != length2:
            cluster_center_init = Tools.get_new_center(features, cluster_label, k)
            length1 = k = len(cluster_center_init)
            clustering = sklearn_cluster.KMeans(n_clusters=k, init=cluster_center_init, n_init=1).fit(features)
            cluster_label = clustering.labels_

            cluster_center_init = Tools.get_new_center(features, cluster_label, k)
            length2 = k = len(cluster_center_init)
            clustering = sklearn_cluster.KMeans(n_clusters=k, init=cluster_center_init, n_init=1).fit(features)
            cluster_label = clustering.labels_
            if log:
                log.dump("Description", f"split outliers: {length1} | {length2}")

        if verbose: print('Split finished. No more outliers could be found in the cluster according to the given criteria.')


        #Merge cluster centers that are very close
        length1 = -1
        length2 = -2
        while length1 != length2:
            new_cluster_center_init = Tools.merge_cluster(features, cluster_label, k, identical_asset, argsort)
            new_cluster_center_init = new_cluster_center_init[~np.isnan(new_cluster_center_init).any(axis=1)]
            length1 = k = len(new_cluster_center_init)
            clustering = sklearn_cluster.KMeans(n_clusters=k, init=new_cluster_center_init, n_init=1).fit(features)
            cluster_label = clustering.labels_

            new_cluster_center_init = Tools.merge_cluster(features, cluster_label, k, identical_asset, argsort)
            new_cluster_center_init = new_cluster_center_init[~np.isnan(new_cluster_center_init).any(axis=1)]
            length2 = k = len(new_cluster_center_init)
            clustering = sklearn_cluster.KMeans(n_clusters=k, init=new_cluster_center_init, n_init=1).fit(features)
            cluster_label = clustering.labels_
            if log:
                log.dump("Description", f"Converge centers: {length1} | {length2}")

        if verbose: print('Merging finished. No more centroids could be merged cross different clusters according to the given criteria.')

        if verbose: print('Start to merge outlier clusters.')
        cluster_label = Tools.merge_outlier(cluster_label, features, log)
        self.label = cluster_label
        k = len(np.unique(cluster_label))
        self.k = k
        if verbose: print(f'There are {k} final clusters')

        if log:
            Tools.cluster_holding_asset_distribution_boxplot(features, cluster_label, k, self.cache.asset_type)

        self.hasBeenFit = True

        return cluster_label

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
        raise NotImplementedError("Subclasses should implement output_result")
