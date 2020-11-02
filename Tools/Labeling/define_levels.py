

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
