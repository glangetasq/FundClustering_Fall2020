

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
