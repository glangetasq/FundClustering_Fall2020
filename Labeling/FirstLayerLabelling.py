""" Implementation of result visualization for the first layer clustering """


import numpy as np
import os
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# Local imports
from BaseClasses import FundClusterVisualizationHelperBased
from DataHelper import DataHelper
from DataHelper.LabelingDataHelper import LabelingDataHelper
from Models.HoldingDataMainClustering import HoldingDataMainClustering
from Tools import Labeling


class FirstLayerLabeling(FundClusterVisualizationHelperBased):
    """ Cluster level labeling & result visualization """

    def __init__(self, cluster_method):
        """Init function to link the helper to a specific fund clustering strategy obj,
            or mutliple clustering method, these obj could either be just created and
            trained in memory, or load from pickle

        Parameters:
            cluster_method: FundClusterBased or derived class obj
                represent the cluster method that we want to register
        """
        self._cluster_method = cluster_method
        self._set_up = False

    def set_up(self, clustering_year, source_type, fit = True, file = None, **kwargs):
        """Set up first layer clustering and get data ready for result visualization"""

        self.clustering_year = clustering_year

        if fit == True:
            # Instantiate and do first layer clustering
            first_layer = HoldingDataMainClustering()
            first_layer.load_raw_data(self.clustering_year)
            first_layer.set_up()

            # Fit the first layer. Takes approximately 5-10 minutes.
            self.label = first_layer.fit()

            # Update the label for result visualization
            self.label = first_layer.output_result(output_cluster = True)

            # Get required data for later methods
            self.mrnstar_data = first_layer.data.fund_mrnstar
            self.cumret_data = first_layer.data.cumul_returns
            self.ret_data = first_layer.data.returns
            self.asset_type = first_layer.asset_type
            self.fundno_ticker = first_layer.data.fundno_ticker
        else:
            # if we don't fit inside set_up, read in the clustering results from a given file
            self.label = pd.read_csv(file)
            # Fetch and Processing
            if source_type.lower() == 'csv':
                self.data = DataHelper.get_data_cache(source='csv', clustering_year=clustering_year)
            elif source_type.lower() == 'sql':
                self.password = kwargs.get('password', None)
                self.username = kwargs.get('username', None)
                self.schema = kwargs.get('schema', None)
                self.data = DataHelper.get_data_cache(source='sql', clusting_year=clustering_year, username = self.username, password = self.password, schema = self.schema)
            else:
                raise ValueError(f"The type of source '{source_type}' is not supported at the moment.")
            
            processor = DataHelper.get_data_processor()
            self.features = processor.holding_asset_pivot(self.data)
            self.data.returns = self.data.returns[self.features.index]
            self.data.cumul_returns = self.data.cumul_returns[self.features.index]

            # Get required data for later methods
            self.mrnstar_data = self.data.fund_mrnstar
            self.cumret_data = self.data.cumul_returns
            self.ret_data = self.data.returns
            self.asset_type = list(self.data.holding_asset.columns)[2:]
            self.fundno_ticker = self.data.fundno_ticker

        # df is the processed assets holding for all funds and for all the years covered
        # df_year is the processed assets holding for all funds in a specific year
        # feature_nostd is the features for all funds and for all the years covered
        self.df, self.df_year, self.feature_nostd = LabelingDataHelper(self.clustering_year)

        self._set_up = True
        self.characteristics = False

        print('Set up done for result visualization')
        return None


    def get_fund_label(self, loc = 'final_output', save_results = True):
        """Generate lable information for each fund, and return the cluster label
        for each fund, and also the charatersitics of each fund

        output: the fund labeling returned by the first layer clustering (without subclusters)
        """

        if self._set_up == False:
            print('Please first set up!')
            return None

        if not os.path.exists(loc):
            os.makedirs(loc)

        if save_results == True:
            self.label.to_csv(f'{loc}/cluster_result_{self.clustering_year}.csv', index=False)
            print('Sucessfully saved the clustering output!')

        return self.label


    def generate_cluster_label(self):
        """Generate label information for cluster, and print the cluster label name
        for each cluster, and also the charatersitics of each label

        output: cluster summary including: cluster name,
                                        number of funds in each cluster,
                                        median asset allocation percentages of each cluster,
                                        cluster description based on investment focus
        """

        if self._set_up == False:
            print('Please first set up!')
            return None

        self.label['Fund.No'] = self.label['Fund.No'].apply(float)
        merged = self.label.reset_index()[['Cluster','Fund.No']].merge(self.df_year.reset_index(),how='left', left_on = 'Fund.No', right_on = 'crsp_fundno').drop('crsp_fundno', axis=1)

        # Median of asset allocation percentages of each Cluster
        summary_cluster = merged.groupby('Cluster').median().drop(['Fund.No', 'index'], axis=1)

        # Number of funds in each cluster
        summary_cluster['No. of funds'] = self.label['Cluster'].value_counts()

        # Adding cluster descriptions based on investment focus
        summary_cluster = Labeling.asset_focus_description(summary_cluster)

        return summary_cluster



    def get_fund_list(self, cluster_name):
        """Get funds based on cluster name provide

        Parameters:
            cluster_name: str
                name of the cluster defined in the cluster label
        """

        if self._set_up == False:
            print('Please first set up!')
            return None

        fund = self.label[self.label['Cluster'] == cluster_name]

        return fund


    def generate_cluster_characteristics(self):
        """ Set-up function for generating cluster characteristics
            must be implemented before get_cluster_characteristics()
        """

        if self._set_up == False:
            print('Please first set up!')
            return None

        merged = self.label.reset_index()[['Cluster','Fund.No']].merge(self.df_year.reset_index(),how='left', left_on = 'Fund.No', right_on = 'crsp_fundno').drop('crsp_fundno', axis=1)

        # Median of asset allocation percentages of each Cluster
        summary_cluster = merged.groupby('Cluster').median().drop(['Fund.No', 'index'], axis=1)

        # Number of funds in each cluster
        summary_cluster['No. of funds'] = self.label['Cluster'].value_counts()

        # Adding cluster descriptions based on investment focus
        summary_cluster = Labeling.asset_focus_description(summary_cluster)

        # Adding risk & return profile
        summary_cluster = Labeling.risk_return_profile(summary_cluster, self.label, self.feature_nostd, subcluster=False)

        # Adding the most frequent Morningstar category & Category (labels provided in crsp data file):
        morningstar = list(); cluster_category = list()

        for pairs in list(np.unique(summary_cluster.index)):
            cluster = pairs
            a,b = labelling.fund_categories(self.label, cluster)
            morningstar.append(a.index[0])
            cluster_category.append(b.index[0])

        summary_cluster['Top Morningstar Category'] = morningstar
        summary_cluster['Top Cluster Category'] = cluster_category

        # See if these funds are actively managed or not
        #           by looking at the degree of change in asset allocation %s over the years.
        # The idea is that we can tell how actively the fund is managed based on how much asset allocation has shifted over the years.
        average_std = self.df.groupby('crsp_fundno').std().mean(axis=1).reset_index()
        temp = merged[['Cluster','Fund.No']].merge(average_std, how='inner',left_on='Fund.No',right_on='crsp_fundno').rename(columns = {0:'allocation_chg_std'})
        temp = temp.groupby(['Cluster']).mean()['allocation_chg_std']
        summary_cluster = summary_cluster.merge(temp, how = 'inner', left_on=['Cluster'], right_on=['Cluster'])
        summary_cluster['Active_management'] = labelling.define_levels(summary_cluster['allocation_chg_std'])
        summary_cluster = summary_cluster[['Cluster Description','Single Asset Focus', 'Multi Asset Focus', 'Shorted Asset',
                           'volatility', 'annual_return', 'max_dd', 'vol_median','return_median', 'max_dd_median',
                           'Top Morningstar Category', 'Top Cluster Category','allocation_chg_std', 'Active_management',
                           'Common Stock', 'Preferred Stock','Convertible Bonds', 'Corporate Bonds', 'Muni Bonds',
                           'Gov Bonds','Other Securities', 'Cash', 'ABS', 'MBS', 'Other Equity', 'Other FI']]
        summary_cluster.dropna(inplace=True)

        self.summary_cluster = summary_cluster
        self.characteristics = True
        print('Successfully generated cluster characteristics!')

        return None


    def get_cluster_characteristics(self, cluster_name, pieplot = False):
        """Get funds characterisitics based on cluster name provide

        Parameters:
            cluster_name: str
                name of the cluster defined in the cluster label
        """

        if self.characteristics == False:
            print('Please first generate cluster characteristics!')
            return None

        # extract characteristics data for the required cluster
        cluster = self.summary_cluster[self.summary_cluster.index == cluster_name]

        # show the pieplot of asset allocation of the cluster if required
        if pieplot == True:
            Labeling.pie_chart(self.label, self.df_year, cluster_name)

        return cluster


    def get_top_funds_in_cluster(self, cluster_name):
        """Based on fund ranking provided in database, provide the top fund in the cluster,
        this need connection to alternative data project, could just return list of fund for now"""

        # just return list of fund for now
        if self._set_up == False:
            print('Please first set up!')
            return None

        fund = self.label[self.label['Cluster'] == cluster_name]

        return fund
