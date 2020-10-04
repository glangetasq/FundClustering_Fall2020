""" Implementation of second layer clustering by return data """

from BaseClasses import FundClusterBased
from DataHelper import *
import Tools
from time import time

import numpy as np
import pandas as pd
from sklearn import cluster as sklearn_cluster


class SecondLayerClustering(FundClusterBased):

    """Clustering algorithm to define the cluster of a specific clustering method used to define cateogry of mutual fund"""
    def __init__(self):

        super().__init__("SecondLayerClustering")

        self.status = "Needs to load data."

    def set_up(self, **kwargs):
        """Function to setup any private variable for the allocator"""

        self.features = None
        self.features_nostd = None
        self.label = None
        self.k = None

        # set up the features
        self._set_up_features(**kwargs)

        self.status = "Needs to be fit."


    def _set_up_features(self, **kwargs):

        
      

        features.dropna(axis=0, inplace=True)
        self.features = features
        self.data.returns = self.data.returns[self.features.index]
        self.data.cumul_returns = self.data.cumul_returns[self.features.index]

        self.features_nostd = self.features.copy()
        self.features = Tools.normal_standardization(self.features)
        self.features = np.round(self.features, 4)

        return self.features, self.features_nostd


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
        
        
        subcluster_dict = dict()
        for group in range(len(set(firstlayer_label))):
            slc = second_layer_clustering(clustering_year=args.year, ret_data=data_trimmed, asset_data=holding_asset, 
                                        mrnstar_class_data=fund_mornstar, feature_first_layer=feature_nostd, 
                                        first_layer_result=firstlayer_label, group=group)
            compressed_data, fundnos = slc.get_timeseries(ret=True, val=True)
            
            #Check if the sample is bigger than 1
            if compressed_data.shape[0] == 1:
                subcluster_dict[fundnos[0]] = 0
                continue
            
            #determine the pool size
            from Tools import isPrime
            if isPrime.isPrime(compressed_data.shape[1]):
                compressed_data = compressed_data[:, :compressed_data.shape[1]-1, :]
            for i in range(10, compressed_data.shape[1]//2):
                if compressed_data.shape[1]%i == 0:
                    args.pool_size = i
                    break
            
            #initialize model
            from Tools.dtc import DTC
            args.n_clusters = min(15, sum(firstlayer_label==group)//2)
            dtc = DTC(n_clusters=args.n_clusters,
                    input_dim=compressed_data.shape[-1],
                    timesteps=compressed_data.shape[1],
                    n_filters=args.n_filters,
                    kernel_size=args.kernel_size,
                    strides=args.strides,
                    pool_size=args.pool_size,
                    n_units=args.n_units,
                    alpha=args.alpha,
                    dist_metric=args.dist_metric,
                    cluster_init=args.cluster_init)

            #Train autoencoder
            dtc.initialize_autoencoder()
            if args.ae_weights is None and args.pretrain_epochs > 0:
                dtc.pretrain(X=compressed_data, optimizer=args.pretrain_optimizer,
                            epochs=args.pretrain_epochs, batch_size=args.batch_size,
                            save_dir=args.save_dir)
            elif args.ae_weights is not None:
                dtc.load_ae_weights(args.ae_weights)

            #Fetch the compressed data/result from the autoencoder
            secondlayer_features = dtc.encode(compressed_data)

            #Compile model
            dtc.compile_clustering_model(optimizer=args.optimizer)

            #Apply hierarchical clustering to select initial cluster centers used in KMeans
            dtc.init_cluster_weights()

            #Train clustering algorithm by using KL divergence as loss
            t0 = time()
            dtc.fit(secondlayer_features, None, None, None, args.epochs, args.eval_epochs, args.save_epochs, args.batch_size,
                    args.tol, args.patience, args.save_dir)
            print('Training time: ', (time() - t0))

            #Get the clustering result
            pred_p = dtc.model.predict(secondlayer_features)
            subcluster_label = pred_p.argmax(axis=1)
            subcluster_label = slc.organize_label(subcluster_label)

            #Plot it out to check
            # slc.plot_sub_result()

            #Write into the dictionary
            for i in range(len(fundnos)):
                subcluster_dict[fundnos[i]] = subcluster_label[i]
       

        # return subcluster label

        self.status = "Has been fit."

        return subcluster_dict

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