""" Result handling helper function for first layer clustering """

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

    
def label_cluster(l, data_nostd):
    k = len(np.unique(l))
    labelling = {}
    ref = {0:data_nostd.columns[0], 
            1:data_nostd.columns[1],
            2:data_nostd.columns[2],
            3:data_nostd.columns[3]}
    for i in range(k):
        index = data_nostd[l==i].median(axis=0)
        if index[0] <= -20:
            if index[1] >= 80:
                labelling[i] = 'Leveraged ' + ref[1] + ' group'
            elif index[2] >= 80:
                labelling[i] = 'Leveraged ' + ref[2] + ' group'
            elif index[3] >= 80:
                labelling[i] = 'Leveraged ' + ref[3] + ' group'
            else:
                labelling[i] = 'Leveraged mixed group'
        elif max(index) >= 80:
            labelling[i] = np.argmax(index) + ' driven group'
        elif sum(list(map(lambda x: x >= 10, index))) >= 3:
            labelling[i] = 'Deversified group'
        elif sum(list(map(lambda x: x >= 25, index))) >= 2:
            if index[0] >= 25 and index[1] >= 25:
                labelling[i] = ref[0] + ' ' + ref[1] + ' mixed group'
            elif index[0] >= 25 and index[2] >= 25:
                labelling[i] = ref[0] + ' ' + ref[2] + ' mixed group'
            elif index[0] >= 25 and index[3] >= 25:
                labelling[i] = ref[0] + ' ' + ref[3] + ' mixed group'
            elif index[1] >= 25 and index[2] >= 25:
                labelling[i] = ref[1] + ' ' + ref[2] + ' mixed group'
            elif index[1] >= 25 and index[3] >= 25:
                labelling[i] = ref[1] + ' ' + ref[3] + ' mixed group'
            elif index[2] >= 25 and index[3] >= 25:
                labelling[i] = ref[2] + ' ' + ref[3] + ' mixed group'
        else:
            labelling[i] = 'Mixed investment group'
    return labelling



def get_sharpe_ret(cumret_df, ret_df, cluster_label):
    if cumret_df.shape[1] != ret_df.shape[1] != len(cluster_label):
        raise ValueError('The input data are not consistent')

    sharpe_dict = {}
    absolute_return = {}
    for i in range(len(np.unique(cluster_label))):
        temp_dict = {}
        df = cumret_df[cumret_df.columns[cluster_label == i]]
        annual_return = (df.iloc[-1, :]) - 1
        annual_vol = ret_df[ret_df.columns[cluster_label == i]].std(axis=0)*np.sqrt(250)
        rf = 0.05 #assumption
        annual_sharpe_ratio = (annual_return - rf)/annual_vol
        pct_25 = np.round(annual_sharpe_ratio.describe()['25%'], 4)
        pct_75 = np.round(annual_sharpe_ratio.describe()['75%'], 4)
        low = np.round(pct_25 - (pct_75 - pct_25)*1.5, 4)
        high = np.round(pct_75 + (pct_75 - pct_25)*1.5, 4)
        for fund in annual_sharpe_ratio.index:
            if annual_sharpe_ratio[fund] >= pct_25 and pct_75 > annual_sharpe_ratio[fund]:
                sharpe_dict[fund] = f'medium: {pct_25}-{pct_75}'
            elif annual_sharpe_ratio[fund] >= pct_75 and high > annual_sharpe_ratio[fund]:
                sharpe_dict[fund] = f'high: {pct_75}-{high}'
            elif annual_sharpe_ratio[fund] >= low and pct_25 > annual_sharpe_ratio[fund]:
                sharpe_dict[fund] = f'low: {low}-{pct_25}'
            elif annual_sharpe_ratio[fund] >= high:
                sharpe_dict[fund] = f'very high: >{high}'
            elif annual_sharpe_ratio[fund] < low:
                sharpe_dict[fund] = f'very low: <{low}'

        temp_dict['med'] = list(annual_sharpe_ratio.index[(pct_75 > annual_sharpe_ratio) & (annual_sharpe_ratio >= pct_25)])
        temp_dict['high'] = list(annual_sharpe_ratio.index[(high > annual_sharpe_ratio) & (annual_sharpe_ratio >= pct_75)])
        temp_dict['very high'] = list(annual_sharpe_ratio.index[annual_sharpe_ratio >= high])
        temp_dict['low'] = list(annual_sharpe_ratio.index[(pct_25 > annual_sharpe_ratio) & (annual_sharpe_ratio >= low)])
        temp_dict['very low'] = list(annual_sharpe_ratio.index[annual_sharpe_ratio < low])
        for key in temp_dict.keys():
            temp_df = cumret_df[temp_dict[key]]
            final_return = (temp_df.iloc[-1, :]) - 1
            threshold = final_return.median()
            for j in final_return.index:
                if final_return[j] >= threshold:
                    absolute_return[j] = ('high', np.round(final_return[j], 4))
                else:
                    absolute_return[j] = ('low', np.round(final_return[j], 4))
    return sharpe_dict, absolute_return


def fund_categories(df, cluster, subcluster=None, col_names = ['Mstar Category', 'Cluster Category']):
    """ For each cluster or subcluster, 
    taking a look at the most popular Morningstar Category and Cluster Category. """
    
    if subcluster == None: 
        df = df.reset_index()
        df = df.set_index(['Cluster'])
        temp = df[df.index.isin([cluster], level=0)]
    else: 
        df = df.reset_index()
        df = df.set_index(['Cluster','Subcluster'])
        temp = df.loc[(cluster, subcluster)]
    
    #Morningstar category
    morningstar = temp.groupby(col_names[0]).size().sort_values(ascending=False)
    
    #Cluster category
    cluster_category = temp.groupby(col_names[1]).size().sort_values(ascending=False)
    
    return morningstar, cluster_category



def pie_chart(labels, df, cluster, subcluster = None, plot=True): 
    '''
    visualization of median asset allocation percentages of each cluster/subcluster
    
    Returns 1) sorted table of median asset allocation percentages of a cluster
               2) pie chart of the asset allocation'''
    
    if subcluster: 
        funds = set(labels.loc[cluster,subcluster]['Fund.No']).intersection(set(df.crsp_fundno))
    else: 
        funds = set(labels[labels.index.isin([cluster], level=0)]['Fund.No']).intersection(set(df.crsp_fundno))
        
    temp = df[df.crsp_fundno.isin(funds)].drop('crsp_fundno',axis=1)
    # temp = df[df.crsp_fundno.isin(funds, level=0)]
    if 'year' in temp.columns: 
        temp = temp.drop('year', axis=1)

    #looking at median investment percentages of asset categories + scaling for piechart purposes
    pieplot = (temp.describe().loc['50%']/(temp.describe().loc['50%'].sum())).sort_values(ascending=False)
    print('<<Median holding asset percentages>>')
    print(pieplot)
    
    pct_value = pieplot.quantile(0.75)
    values_below_pct_value = list(pieplot[(pieplot < pct_value)].index.values)
    pieplot['Other'] = pieplot[values_below_pct_value].sum()
    pieplot = pieplot.drop(values_below_pct_value)
    
    #predefine colors for all assets so the colors do not change for each cluster
    palette = {'Common Stock':'palegreen','Preferred Stock':'royalblue', 'Convertible Bonds':'lightcoral',
                'Corporate Bonds':'violet','Muni Bonds':'yellow', 'Gov Bonds':'orange', 
                'Other Securities':'mediumorchid', 'Cash':'lightslategray', 'ABS':'indianred', 'MBS':'lemonchiffon', 
                'Other Equity':'tomato', 'Other FI':'mistyrose','Other':'slateblue'}
    colors = list()
    for i in range(len(pieplot.index)): 
        col = palette[pieplot.index[i]]
        colors.append(col)    
    plt.figure(figsize = (6,6))
    plt.pie(pieplot, labels=list(pieplot.index), autopct='%1.1f%%', colors = colors)
    plt.legend()
    if subcluster: 
        plt.title(f'Cluster {cluster} Subcluster {subcluster} Asset Allocation')        
    else: 
        plt.title(f'Cluster {cluster} Asset Allocation') 
        plt.show()



def define_levels(array): 
    """returns High/ Mid/ Low categories based on 33%, 66%, 100% percentiles"""
    low_thresh = array.quantile(1/3)
    mid_thresh = array.quantile(2/3)
    temp = list()
    for i in array:
        if i <= low_thresh: 
            temp.append('Low')
        elif i<= mid_thresh: 
            temp.append('Mid')
        else: 
            temp.append('High')
    return temp    



def asset_focus_description(df):
    """ 
    Asset focus: asset allocation characteristics of each cluster:
    #### All clusters fall into one of the following descriptions
    1. Heavily invested in one asset type: if, on average, greater than 75% of funds are invested in one type of asset. 
    2. 80%> investment in ... : if top two asset types make up more than 80% of the cluster
    3. Evenly diversified: no one asset type takes up more than 50% of the fund.
    4. Uneven multi-asset: mix of multiple asset types but not evenly diversified across asset types
    5. Shorted ... : If the average fund has a sizeable short position on a certain asset, added this description
    
    """

    df['Cluster Description'] = ''
    df['Single Asset Focus'] = ''
    df['Multi Asset Focus'] = ''
    df['Shorted Asset']=''

    for i in range(len(df)):
        ordered = df.iloc[i][:12].sort_values(ascending=False)
        short=0
        
        #If shorting an asset class by more than 10%, 
        if any(ordered < -10):
            short = float(ordered[ordered<-10][0])
            shorted_asset = ordered[ordered< -10].index[0]
            df['Shorted Asset'].iloc[i] = shorted_asset
            ordered = ordered[ordered > -10]
        
        if ordered[0] > 75 - short:
            df['Cluster Description'].iloc[i] += 'Heavily invested (75%>) in '+ordered.index[0]
            df['Single Asset Focus'].iloc[i] = ordered.index[0]

        elif ordered[:2].sum() > 80 - short:
            df['Cluster Description'].iloc[i] += '80%> investment in '+ordered.index[0]+' and '+ordered.index[1]
            df['Multi Asset Focus'].iloc[i] = ordered.index[0]+', '+ordered.index[1]

        elif all(ordered < 50): 
        #if spread out over multiple assets withouth concentrating too much on one, say everything is below 50%:
            df['Cluster Description'].iloc[i] += 'Evenly diversified multi-asset: '+ ', '.join([*ordered[ordered.cumsum() < 80-short].index])
            df['Multi Asset Focus'].iloc[i] = ', '.join([*ordered[ordered.cumsum() < 80-short].index])
        
        else: 
            df['Cluster Description'].iloc[i] += 'Uneven multi-asset: '+', '.join([*ordered[ordered.cumsum()<(75-short)].index])
            df['Multi Asset Focus'].iloc[i] = ', '.join([*ordered[ordered.cumsum()<(75-short)].index])
        
        if short:
            df['Cluster Description'].iloc[i] += ', shorted '+ shorted_asset

    return df



def risk_return_profile(df, label, features_nostd, subcluster = False):
    """ Add risk and return characteristics for each cluster """

    features_nostd['index'] = features_nostd.index.astype(int)
    if subcluster == True: 
        label_features_nostd = label.reset_index()[['Cluster','Subcluster','Fund.No']].merge(features_nostd, how='left', left_on = 'Fund.No', right_on = 'index').drop(['index','Fund.No'], axis=1)
        label_features_nostd = label_features_nostd.groupby(['Cluster', 'Subcluster']).median()
    else:
        label_features_nostd = label.reset_index()[['Cluster','Fund.No']].merge(features_nostd, how='left', left_on = 'Fund.No', right_on = 'index').drop(['index','Fund.No'], axis=1)
        label_features_nostd = label_features_nostd.groupby(['Cluster']).median()

    df['volatility'] = define_levels(label_features_nostd['vol'])
    df['annual_return'] = define_levels(label_features_nostd['annual_ret'])
    df['max_dd'] = define_levels(label_features_nostd['max_dd'])
    df['vol_median'] = label_features_nostd['vol'].round(3)
    df['return_median'] = label_features_nostd['annual_ret'].round(3)
    df['max_dd_median'] = label_features_nostd['max_dd'].round(3)

    return df