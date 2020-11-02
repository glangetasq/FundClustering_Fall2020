

def fund_categories(df, cluster, subcluster=None, col_names = ['Mstar Category', 'Cluster Category']):
    """ For each cluster or subcluster,
    taking a look at the most popular Morningstar Category and Cluster Category. """

    if subcluster == None:
        df = df.set_index(['Cluster'])
        temp = df[df.index.isin([cluster], level=0)]
    else:
        df = df.set_index(['Cluster','Subcluster'])
        temp = df.loc[(cluster, subcluster)]

    #Morningstar category
    morningstar = temp.groupby(col_names[0]).size().sort_values(ascending=False)

    #Cluster category
    cluster_category = temp.groupby(col_names[1]).size().sort_values(ascending=False)

    return morningstar, cluster_category
