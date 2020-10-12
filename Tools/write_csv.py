""" Result handling helper function for first layer clustering """

import numpy as np
import pandas as pd

def write_csv(fundno_ticker, loc='final_output'):
    
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