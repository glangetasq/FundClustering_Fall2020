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

        self.status = "Needs to load data."

    def set_up(self, **kwargs):
        """Function to setup any private variable for the allocator"""

        self.asset_type = list(self.data.holding_asset.columns)[2:]
        self.features = None
        self.features_nostd = None
        self.label = None
        self.k = None

        # set up the features
        self._set_up_features(**kwargs)


        self.status = "Needs to be fit."


    def _set_up_features(self, **kwargs):

        features = pd.DataFrame( index = self.data.returns.columns )
        funds = set(self.data.holding_asset.crsp_fundno.values)

        for index in features.index:
            if int(index) in funds:
                for a in self.asset_type:
                    features.loc[index, a] = self.data.holding_asset[self.data.holding_asset.crsp_fundno == int(index)][a].values[0]
            else:
                for a in self.asset_type:
                    features.loc[index, a] = np.NaN

        features.dropna(axis=0, inplace=True)
        self.features = features
        self.data.returns = self.data.returns[self.features.index]
        self.data.cumul_returns = self.data.cumul_returns[self.features.index]

        return self.features

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
        return self.status == "Has been fit."

    def load_raw_data(self, clustering_year, source_type, **kwargs):
        """Function to load raw data from source, should be able to support
        reading data from flat file or sql database. Please just implement the one using flat file now,
        later we would provide the sql python package that we would want to utilize for the database task

        Parameters:
            source_type: str
                flat file type or sql, if it is flat file, file directory or
                path need to be passed in as argument or in the setup function
                If it is sql, connection need to be extablished in setup function
                please avoid any hard coded name in the class, and set global variable to define those file name
        """

        self.clustering_year = clustering_year

        data = DataHolder()
        data.returns = DataHelper.get_returns(clustering_year=self.clustering_year)
        data.cumul_returns = DataHelper.get_cumul_returns(clustering_year=self.clustering_year)
        data.holding_asset = DataHelper.get_holding_asset(clustering_year=self.clustering_year)
        data.mrnstar = DataHelper.get_mrnstar_class(clustering_year=self.clustering_year)

        self.data = data
        self.status = "Needs to be set up."

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

        TODO: Could modularize even more this function.
        """

        # kwargs
        log = kwargs.get('log', None)
        identical_asset = kwargs.get('identical_asset', 3)
        argsort = kwargs.get('argsort', False)

        k = Tools.silhouette(self.normalized_features, log)
        h_clustering = sklearn_cluster.AgglomerativeClustering(n_clusters=k, linkage='ward').fit(self.normalized_features)
        cluster_label = h_clustering.labels_
        print('Best number of clusters for hierarchical clustering is', k)

        #Screen out the outliers
        length1 = -1
        length2 = -2
        print('Starting searching and grouping outliers')
        #Look for the outliers
        while length1 != length2:
            cluster_center_init = Tools.get_new_center(self.features, cluster_label, k)
            length1 = k = len(cluster_center_init)
            clustering = sklearn_cluster.KMeans(n_clusters=k, init=cluster_center_init, n_init=1).fit(self.features)
            cluster_label = clustering.labels_

            cluster_center_init = Tools.get_new_center(self.features, cluster_label, k)
            length2 = k = len(cluster_center_init)
            clustering = sklearn_cluster.KMeans(n_clusters=k, init=cluster_center_init, n_init=1).fit(self.features)
            cluster_label = clustering.labels_
            if log:
                log.dump("Description", f"split outliers: {length1} | {length2}")

        print('Split finished. No more outliers could be found in the cluster according to the given criteria.')


        #Merge cluster centers that are very close
        length1 = -1
        length2 = -2
        while length1 != length2:
            new_cluster_center_init = Tools.merge_cluster(self.features, cluster_label, k, identical_asset, argsort)
            new_cluster_center_init = new_cluster_center_init[~np.isnan(new_cluster_center_init).any(axis=1)]
            length1 = k = len(new_cluster_center_init)
            clustering = sklearn_cluster.KMeans(n_clusters=k, init=new_cluster_center_init, n_init=1).fit(self.features)
            cluster_label = clustering.labels_

            new_cluster_center_init = Tools.merge_cluster(self.features, cluster_label, k, identical_asset, argsort)
            new_cluster_center_init = new_cluster_center_init[~np.isnan(new_cluster_center_init).any(axis=1)]
            length2 = k = len(new_cluster_center_init)
            clustering = sklearn_cluster.KMeans(n_clusters=k, init=new_cluster_center_init, n_init=1).fit(self.features)
            cluster_label = clustering.labels_
            if log:
                log.dump("Description", f"Converge centers: {length1} | {length2}")

        print('Merging finished. No more centroids could be merged cross different clusters according to the given criteria.')

        print('Start to merge outlier clusters.')
        cluster_label = Tools.merge_outlier(cluster_label, self.features, log)
        self.label = cluster_label
        k = len(np.unique(cluster_label))
        self.k = k
        print('The final clusters are', k)

        if log:
            Tools.cluster_holding_asset_distribution_boxplot(self.features, cluster_label, k, self.asset_type)

        # return cluster_label

        self.status = "Has been fit."

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
