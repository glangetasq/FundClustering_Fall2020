class FundClusterVisualizationHelperBased:
    """Based class to define result visualization for the fund cluster strategy"""
    
    def __init__(self, cluster_method):
        """Init function to link the helper to a specific fund clustering strategy obj, 
            or mutliple clustering method, these obj could either be just created and 
            trained in memory, or load from pickle
        
        Parameters:
            cluster_method: FundClusterBased or derived class obj
                represent the cluster method that we want to register
        """
        self._cluster_method = cluster_method
    
    def generate_cluster_label(self):
        """Generate lable information for cluster, and print the cluster label name 
        for each cluster, and also the characterisitics of each label"""
        raise NotImplementedError("Subclasses should implement generate_cluster_label!")
    
    def get_fund_list(self, cluster_name):
        """Get funds based on cluster name provide
        
        Parameters:
            cluster_name: str
                name of the cluster defined in the cluster label
        """
        raise NotImplementedError("Subclasses should implement get_fund_list!")
    
    def get_cluster_characteristics(self, cluster_name):
        """Get funds charactersitics based on cluster name provide
        
        Parameters:
            cluster_name: str
                name of the cluster defined in the cluster label
        """
        raise NotImplementedError("Subclasses should implement get_cluster_characteristics!")

    def get_top_funds_in_cluster(self, cluster_name):
        """Based on fund ranking provided in database, provide the top fund in the cluster, 
        this need connection to alternative data project, could just return list of fund for now"""
        raise NotImplementedError("Subclasses should implement get_top_funds_in_cluster!")


