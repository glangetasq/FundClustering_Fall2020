def silhouette(feature, log=None):
    """
    Silhouette function. TODO: describe function
    """

    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics import silhouette_score

    score = []
    mx = 0
    res = None

    max_k = min(len(feature), 30)
    
    if max_k in [0,1,2]:
        return max_k
    else: 
        for i in range(2, max_k+1):
            k = i
            clustering = AgglomerativeClustering(n_clusters=k).fit(feature)
            cluster_label = clustering.labels_
            score.append(silhouette_score(feature, cluster_label, metric='euclidean'))
            if score[-1] >= mx:
                mx = score[-1]
                res = i
    
        if log:
            log.dump("Plot", x=list(range(2, 30)), y=score, xlim=(2,30))
            log.dump("Description", f"The best k determined by statistical approach is {res}")
    
        return res
