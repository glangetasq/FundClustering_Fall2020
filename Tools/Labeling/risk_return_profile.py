

def risk_return_profile(df, label, features_nostd, subcluster = False):
    """ Add risk and return characteristics for each cluster """

    features_nostd['index'] = features_nostd.index.astype(int)
    if subcluster == True:
        label_features_nostd = label.reset_index()[['Cluster','Subcluter','Fund.No']].merge(features_nostd, how='left', left_on = 'Fund.No', right_on = 'index').drop(['index','Fund.No'], axis=1)
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
