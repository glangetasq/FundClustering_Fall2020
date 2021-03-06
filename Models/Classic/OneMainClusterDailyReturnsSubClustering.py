""" Implementation of second layer clustering (sub clustering).
Only for one main cluster
"""

import numpy as np
import pandas as pd
from sklearn import cluster as sklearn_cluster
from time import time

# Local imports
from BaseClasses import FundClusterBased
import Config
from DataHelper import *
import HyperparametersHelper
import Tools


class OneMainClusterDailyReturnsSubClustering(FundClusterBased):

    """Clustering algorithm to define the cluster of a specific clustering method used to define cateogry of mutual fund"""
    def __init__(self):

        super().__init__("SecondLayerClustering")

        self.hasBeenFit = False

    def set_up(self,
            features_first_layer,
            labels_first_layer,
            returns,
            main_cluster,
            **kwargs):
        """Function to setup any private variable for the allocator"""

        self._features = features_first_layer
        self._labels = labels_first_layer
        self._returns = returns
        self._main_cluster = main_cluster

        self.hasBeenFit = False


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

    def load_raw_data(self):
        """Function to load raw data from source, should be able to support
        reading data from flat file or sql database. Please just implement the one using flat file now,
        later we would provide the sql python package that we would want to utilize for the database task
        """

        raise NotImplementedError("This model is only for sub-clustering 1 maincluster.")


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

        subcluster_dict = dict()

        compressed_data, fundnos = Tools.get_timeseries(ret_flag=True,
                val_flag=True,
                ret_data = self._returns,
                feature = self._features,
                label = self._labels,
                main_cluster = self._main_cluster
        )
        self.new_feature = compressed_data
        self.fundnos = fundnos

        #Check if the sample is bigger than 1
        if compressed_data.shape[0] == 1:
            subcluster_dict[fundnos[0]] = 0
            #print("There was a continue before")
            return subcluster_dict

        #determine the pool size
        if Tools.isPrime(compressed_data.shape[1]):
            compressed_data = compressed_data[:, :compressed_data.shape[1]-1, :]

        if compressed_data.shape[1] <= 10:
            hyper_parameters.pool_size = compressed_data.shape[1]
        else:
            for i in range(10, compressed_data.shape[1]//2):
                if compressed_data.shape[1] % i == 0:
                    hyper_parameters.pool_size = i
                    break


        print('Timesteps = ', compressed_data.shape[1])
        print('Pool size = ', hyper_parameters.pool_size)
        #initialize the DTC model
        from DTC.dtc import DTC
        hyper_parameters.n_clusters = min(15, sum(self._labels==self._main_cluster)//2)
        print('N clusters in DTC for', self._main_cluster, 'is', hyper_parameters.n_clusters)
        dtc = DTC(n_clusters=hyper_parameters.n_clusters,
                input_dim=compressed_data.shape[-1],
                timesteps=compressed_data.shape[1],
                n_filters=hyper_parameters.n_filters,
                kernel_size=hyper_parameters.kernel_size,
                strides=hyper_parameters.strides,
                pool_size=hyper_parameters.pool_size,
                n_units=hyper_parameters.n_units,
                alpha=hyper_parameters.alpha,
                dist_metric=hyper_parameters.dist_metric,
                cluster_init=hyper_parameters.cluster_init
            )

        #Train autoencoder
        dtc.initialize_autoencoder()
        if hyper_parameters.ae_weights is None and hyper_parameters.pretrain_epochs > 0:
            dtc.pretrain(
                X=compressed_data,
                optimizer=hyper_parameters.pretrain_optimizer,
                epochs=hyper_parameters.pretrain_epochs,
                batch_size=hyper_parameters.batch_size,
                save_dir=hyper_parameters.save_dir
            )
        elif hyper_parameters.ae_weights is not None:
            dtc.load_ae_weights(hyper_parameters.ae_weights)

        #Fetch the compressed data/result from the autoencoder
        secondlayer_features = dtc.encode(compressed_data)

        #Compile model
        dtc.compile_clustering_model(optimizer=hyper_parameters.optimizer)

        #Apply hierarchical clustering to select initial cluster centers used in KMeans
        dtc.init_cluster_weights()

        #Train clustering algorithm by using KL divergence as loss
        t0 = time()
        dtc.fit(
            secondlayer_features,
            None,
            None,
            None,
            hyper_parameters.epochs,
            hyper_parameters.eval_epochs,
            hyper_parameters.save_epochs,
            hyper_parameters.batch_size,
            hyper_parameters.tol,
            hyper_parameters.patience,
            hyper_parameters.save_dir
        )

        print('Training time: ', (time() - t0))

        #Get the clustering result
        from Tools import organize_label
        pred_p = dtc.model.predict(secondlayer_features)
        subcluster_label = pred_p.argmax(axis=1)
        subcluster_label = organize_label(subcluster_label)
        self.subcluster_label = subcluster_label
        self.subcluster_k = len(set(subcluster_label))

        #Write into the dictionary
        for i in range(len(fundnos)):
            subcluster_dict[fundnos[i]] = subcluster_label[i]


        # return subcluster label

        self.hasBeenFit = True
        self.subcluster_dict = subcluster_dict

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

    def output_result(self, save_models=False, path=None, **kwargs):
        """Function to output the model, could use pickle to cached the obj that
        has been trained, so that you could load the obj later directly later, and you could also use this function
        to output the optimal cluster, please use arguments to config what you want to output
        Parameters:
            save_model: bool
                save the model as a pickle to loc
            path: str
                path to save the model, raise Error if not defined and if save_model is True
        """

        Tools.save_model(save_model, path, self)
