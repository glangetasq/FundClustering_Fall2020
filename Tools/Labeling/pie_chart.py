

import matplotlib.pyplot as plt


def pie_chart(labels, df, cluster, subcluster = None, plot=True):
    '''
    visualization of median asset allocation percentages of each cluster/subcluster

    Returns 1) sorted table of median asset allocation percentages of a cluster
               2) pie chart of the asset allocation'''

    if subcluster:
        funds = set(labels.loc[(cluster,subcluster)]['Fund.No']).intersection(set(df.crsp_fundno))
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
