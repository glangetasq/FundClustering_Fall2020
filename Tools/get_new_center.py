import numpy as np

def get_new_center(feature, label, k):
    """
    TODO: Docstring of this Function
    """

    cluster_center_init = []

    for i in range(k):
        df = feature[label == i]
        cur_cluster_center = df.median(axis=0)
        if len(df) == 0:
            continue
        sit = False

        for ass in list(df.columns):
            ass_25 = np.percentile(df[ass], 25)
            ass_75 = np.percentile(df[ass], 75)
            low = max(ass_25 - 1.5*(ass_75-ass_25), df[ass].min())
            high = min(ass_75 + 1.5*(ass_75-ass_25), df[ass].max())

            if ass_75 - ass_25 > 20:
                cluster_center_init.append(df[df[ass] == np.sort(df[ass])[len(df[ass])*3//4]].iloc[0, :])
                cluster_center_init.append(df[df[ass] == np.sort(df[ass])[len(df[ass])*1//4]].iloc[0, :])
                sit = True
            elif high - low >= 50:
                cluster_center_init.append(df[df[ass] == np.sort(df[df[ass] >= high][ass])[sum(df[ass] >= high)//2]].iloc[0, :])
                cluster_center_init.append(df[df[ass] == np.sort(df[df[ass] <= low][ass])[sum(df[ass] <= low)//2]].iloc[0, :])
                sit = True
            elif high - ass_75 > 20 or sum(df[ass] >= high) >= 10:
                cluster_center_init.append(df[df[ass] == np.sort(df[df[ass] >= high][ass])[sum(df[ass] >= high)//2]].iloc[0, :])
                sit = True
            elif ass_25 - low > 20 or sum(df[ass] <= low) >= 10:
                cluster_center_init.append(df[df[ass] == np.sort(df[df[ass] <= low][ass])[sum(df[ass] <= low)//2]].iloc[0, :])
                sit = True
            if sit == True:
                break
        if sit == False:
            cluster_center_init.append(cur_cluster_center)

    cluster_center_init = np.array(cluster_center_init)

    return np.unique(cluster_center_init, axis=0)
