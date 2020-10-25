#DTC Model -- first train the autoencoder to then train the clustering model

import argparse # For input parsing
import csv # For writing log files
# from gap_statistic import OptimalK
# Keras imports
from keras.models import Model
from keras.layers import Input, Dense, Reshape, UpSampling2D, Conv2DTranspose, GlobalAveragePooling1D, Softmax
from keras.losses import kullback_leibler_divergence
import keras.backend as K
# --------------------- #
import numpy as np
import os
import pandas as pd
# Sklearn imports
from sklearn import cluster, metrics
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import davies_bouldin_score, pairwise_distances
# --------------------- #
from time import time
import tslearn
from tslearn.clustering import TimeSeriesKMeans


# Local imports
from .TSClusteringLayer import TSClusteringLayer
from .TAE import temporal_autoencoder
from .metrics import *
from .tsdistances import *


class DTC:
    """
    Deep Temporal Clustering (DTC) model
    # Arguments
        n_clusters: number of clusters
        input_dim: input dimensionality
        timesteps: length of input sequences (can be None for variable length)
        n_filters: number of filters in convolutional layer
        kernel_size: size of kernel in convolutional layer
        strides: strides in convolutional layer
        pool_size: pooling size in max pooling layer, must divide the time series length
        n_units: numbers of units in the two BiLSTM layers
        alpha: coefficient in Student's kernel
        dist_metric: distance metric between latent sequences
        cluster_init: cluster initialization method
    """

    def __init__(self, n_clusters, input_dim, timesteps,
                 n_filters=50, kernel_size=10, strides=1, pool_size=10, n_units=[50, 1],
                 alpha=1.0, dist_metric='eucl', cluster_init='kmeans'):
        assert(timesteps % pool_size == 0)
        self.n_clusters = n_clusters
        self.input_dim = input_dim
        self.timesteps = timesteps
        self.n_filters = n_filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.pool_size = pool_size
        self.n_units = n_units
        self.latent_shape = (self.timesteps // self.pool_size, self.n_units[1])
        self.alpha = alpha
        self.dist_metric = dist_metric
        self.cluster_init = cluster_init
        self.pretrained = False
        self.model = self.autoencoder = self.encoder = self.decoder = None


    #Autoencoder part
    def initialize_autoencoder(self):
        """
        Create DTC model
        """
        # Create AE models
        self.autoencoder, self.encoder, self.decoder = temporal_autoencoder(input_dim=self.input_dim,
                                                                            timesteps=self.timesteps,
                                                                            n_filters=self.n_filters,
                                                                            kernel_size=self.kernel_size,
                                                                            strides=self.strides,
                                                                            pool_size=self.pool_size,
                                                                            n_units=self.n_units)

    def load_ae_weights(self, ae_weights_path):
        """
        Load pre-trained weights of AE
        # Arguments
            ae_weight_path: path to weights file (.h5)
        """
        self.autoencoder.load_weights(ae_weights_path)
        self.pretrained = True

    def pretrain(self, X,
                 optimizer='adam',
                 epochs=500,
                 batch_size=64,
                 save_dir='results',
                 verbose=1):
        """
        Pre-train the autoencoder using only MSE reconstruction loss
        Saves weights in h5 format.
        # Arguments
            X: training set
            optimizer: optimization algorithm
            epochs: number of pre-training epochs
            batch_size: training batch size
            save_dir: path to existing directory where weights will be saved
        """
        print('Pretraining...')
        self.autoencoder.compile(optimizer=optimizer, loss='mse')

        # Begin pretraining
        t0 = time()
        self.autoencoder.fit(X, X, batch_size=batch_size, epochs=epochs, verbose=verbose)
        print('Pretraining time: ', time() - t0)
        # self.autoencoder.save_weights('{}/ae_weights-epoch{}.h5'.format(save_dir, epochs))
        print('Pretrained weights are saved to {}/ae_weights-epoch{}.h5'.format(save_dir, epochs))
        self.pretrained = True

    def encode(self, x):
        """
        Encoding function. Extract latent features from hidden layer
        # Arguments
            x: data point
        # Return
            encoded (latent) data point
        """
        self.features = self.encoder.predict(x)
        return self.features

    def decode(self, x):
        """
        Decoding function. Decodes encoded sequence from latent space.
        # Arguments
            x: encoded (latent) data point
        # Return
            decoded data point
        """
        return self.decoder.predict(x)

    #Clustering part
    def compile_clustering_model(self, optimizer):
        """
        Compile DTC model
        # Arguments
            gamma: coefficient of TS clustering loss
            optimizer: optimization algorithm
            initial_heatmap_loss_weight (optional): initial weight of heatmap loss vs clustering loss
            final_heatmap_loss_weight (optional): final weight of heatmap loss vs clustering loss (heatmap finetuning)
        """
        clustering_input = Input(shape=(self.features.shape[1], self.features.shape[2]), name='clustering_input')

        clustering_layer = TSClusteringLayer(self.n_clusters,
                                             alpha=self.alpha,
                                             dist_metric=self.dist_metric,
                                             name='TSClustering')(clustering_input)

        self.model = Model(inputs=clustering_input,
                           outputs=clustering_layer)
        print(self.model.summary())

        self.model.compile(loss='kld',
                           optimizer=optimizer)

    #Initialize cluster centers
    def init_cluster_weights(self):
        """
        Initialize with complete-linkage hierarchical clustering or k-means.
        # Arguments
            X: numpy array containing training set or batch
        """
        assert(self.cluster_init in ['hierarchical', 'kmeans'])
        print('Initializing cluster...')

        features = self.features

        if self.cluster_init == 'hierarchical':
            if self.dist_metric == 'eucl':  # use AgglomerativeClustering off-the-shelf
                hc = AgglomerativeClustering(n_clusters=self.n_clusters,
                                             affinity='euclidean',
                                             linkage='complete').fit(features.reshape(features.shape[0], -1))
            else:  # compute distance matrix using dist
                d = np.zeros((features.shape[0], features.shape[0]))
                for i in range(features.shape[0]):
                    for j in range(i):
                        d[i, j] = d[j, i] = self.dist(features[i], features[j])
                hc = AgglomerativeClustering(n_clusters=self.n_clusters,
                                             affinity='precomputed',
                                             linkage='complete').fit(d)
            # compute centroid
            cluster_centers = np.array([features[hc.labels_ == c].mean(axis=0) for c in range(self.n_clusters)])
        elif self.cluster_init == 'kmeans':
            # fit k-means on flattened features
            km = KMeans(n_clusters=self.n_clusters, n_init=10).fit(features.reshape(features.shape[0], -1))
            cluster_centers = km.cluster_centers_.reshape(self.n_clusters, features.shape[1], features.shape[2])

        self.model.get_layer(name='TSClustering').set_weights([cluster_centers])
        print('Done!')

    @property
    def cluster_centers_(self):
        """
        Returns cluster centers
        """
        return self.model.get_layer(name='TSClustering').get_weights()[0]

    @staticmethod
    def weighted_kld(loss_weight):
        """
        Custom KL-divergence loss with a variable weight parameter
        """
        def loss(y_true, y_pred):
            return loss_weight * kullback_leibler_divergence(y_true, y_pred)
        return loss

    def load_weights(self, weights_path):
        """
        Load pre-trained weights of DTC model
        # Arguments
            weight_path: path to weights file (.h5)
        """
        self.model.load_weights(weights_path)
        self.pretrained = True

    def dist(self, x1, x2):
        """
        Compute distance between two multivariate time series using chosen distance metric
        # Arguments
            x1: first input (np array)
            x2: second input (np array)
        # Return
            distance
        """
        if self.dist_metric == 'eucl':
            return eucl(x1, x2)
        elif self.dist_metric == 'cid':
            return cid(x1, x2)
        elif self.dist_metric == 'cor':
            return cor(x1, x2)
        elif self.dist_metric == 'acf':
            return acf(x1, x2)
        else:
            raise ValueError('Available distances are eucl, cid, cor and acf!')

    def predict(self, x):
        """
        Predict cluster assignment.
        """
        q = self.model.predict(x, verbose=0)
        return q.argmax(axis=1)

    @staticmethod
    def target_distribution(q):  # target distribution p which enhances the discrimination of soft label q
        weight = q ** 2 / q.sum(0)
        return (weight.T / weight.sum(1)).T

    def fit(self, X_train, y_train=None,
            X_val=None, y_val=None,
            epochs=100,
            eval_epochs=10,
            save_epochs=10,
            batch_size=64,
            tol=0.001,
            patience=5,
            save_dir='results_v2'):
        """
        Training procedure
        # Arguments
           X_train: training set
           y_train: (optional) training labels
           X_val: (optional) validation set
           y_val: (optional) validation labels
           epochs: number of training epochs
           eval_epochs: evaluate metrics on train/val set every eval_epochs epochs
           save_epochs: save model weights every save_epochs epochs
           batch_size: training batch size
           tol: tolerance for stopping criterion
           patience: patience for stopping criterion
           save_dir: path to existing directory where weights and logs are saved
        """
        if not self.pretrained:
            print('Autoencoder was not pre-trained!')

        """ Ignore logging file for now """

        # Logging file
        # logfile = open(save_dir + '/dtc_log.csv', 'w')
        fieldnames = ['epoch', 'T', 'L', 'Lr', 'Lc']
        if X_val is not None:
            fieldnames += ['L_val', 'Lr_val', 'Lc_val']
        if y_train is not None:
            fieldnames += ['acc', 'pur', 'nmi', 'ari']
        if y_val is not None:
            fieldnames += ['acc_val', 'pur_val', 'nmi_val', 'ari_val']
        # logwriter = csv.DictWriter(logfile, fieldnames)
        # logwriter.writeheader()

        y_pred_last = None
        patience_cnt = 0

        print('Training for {} epochs.\nEvaluating every {} and saving model every {} epochs.'.format(epochs, eval_epochs, save_epochs))

        for epoch in range(epochs):

            # Compute cluster assignments for training set
            q = self.model.predict(X_train)
            p = DTC.target_distribution(q)

            # Evaluate losses and metrics on training set
            if epoch % eval_epochs == 0:

                # Initialize log dictionary
                logdict = dict(epoch=epoch)

                y_pred = q.argmax(axis=1)
                if X_val is not None:
                    q_val = self.model.predict(X_val)
                    p_val = DTC.target_distribution(q_val)
                    y_val_pred = q_val.argmax(axis=1)

                print('epoch {}'.format(epoch))
                loss = self.model.evaluate(X_train, p, batch_size=batch_size, verbose=False)
                logdict['L'] = loss
                print('[Train] - total loss={:f}'.format(logdict['L']))
                if X_val is not None:
                    val_loss = self.model.evaluate(X_val, p_val, batch_size=batch_size, verbose=False)
                    logdict['L_val'] = val_loss
                    print('[Val] - total loss={:f}'.format(logdict['L_val']))

                # Evaluate the clustering performance using labels
                if y_train is not None:
                    logdict['acc'] = cluster_acc(y_train, y_pred)
                    logdict['pur'] = cluster_purity(y_train, y_pred)
                    logdict['nmi'] = metrics.normalized_mutual_info_score(y_train, y_pred)
                    logdict['ari'] = metrics.adjusted_rand_score(y_train, y_pred)
                    print('[Train] - Acc={:f}, Pur={:f}, NMI={:f}, ARI={:f}'.format(logdict['acc'], logdict['pur'],
                                                                                    logdict['nmi'], logdict['ari']))
                if y_val is not None:
                    logdict['acc_val'] = cluster_acc(y_val, y_val_pred)
                    logdict['pur_val'] = cluster_purity(y_val, y_val_pred)
                    logdict['nmi_val'] = metrics.normalized_mutual_info_score(y_val, y_val_pred)
                    logdict['ari_val'] = metrics.adjusted_rand_score(y_val, y_val_pred)
                    print('[Val] - Acc={:f}, Pur={:f}, NMI={:f}, ARI={:f}'.format(logdict['acc_val'], logdict['pur_val'],
                                                                                  logdict['nmi_val'], logdict['ari_val']))

                # logwriter.writerow(logdict)

                # check stop criterion
                if y_pred_last is not None:
                    assignment_changes = np.sum(y_pred != y_pred_last).astype(np.float32) / y_pred.shape[0]
                y_pred_last = y_pred
                if epoch > 0 and assignment_changes < tol:
                    patience_cnt += 1
                    print('Assignment changes {} < {} tolerance threshold. Patience: {}/{}.'.format(assignment_changes, tol, patience_cnt, patience))
                    if patience_cnt >= patience:
                        print('Reached max patience. Stopping training.')
                        # logfile.close()
                        break
                else:
                    patience_cnt = 0

            # Save intermediate model and plots
            if epoch % save_epochs == 0:
                # self.model.save_weights(save_dir + '/DTC_model_' + str(epoch) + '.h5')
                print('Saved model to:', save_dir + '/DTC_model_' + str(epoch) + '.h5')

            # Train for one epoch
            self.model.fit(X_train, p, epochs=1, batch_size=batch_size, verbose=False)

        # Save the final model
        # logfile.close()
        print('Saving model to:', save_dir + '/DTC_model_final.h5')
        # self.model.save_weights(save_dir + '/DTC_model_final.h5')
