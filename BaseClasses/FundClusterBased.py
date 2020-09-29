class FundClusterBased:
    """Clustering algorithm to define the cluster of a specific clustering method used to define cateogry of mutual fund"""
    def __init__(self, cluster_method_name):
        self._cluster_method_name = cluster_method_name
    
    def set_up(self, **kwargs):
        """Function to setup any private variable for the allocator"""
        raise NotImplementedError("Subclasses should implement set_up function!")
    
    def cluster_method(self):
        """This provide identifier of the clustering strategy that you are implementing."""
        return self._cluster_method_name
    
    def machine_learning_based(self):
        """This method tells us whether the cluster category is machine learning 
            based and need to run fit to train model parameters or not
            
        Parameters:
            None

            Return
                bool
                True if the strategy need to run fit to be ready for prediction, otherwise No
        """
        raise NotImplementedError("Subclasses should implement machine_learning_based!")
    
    def load_raw_data(self, source_type, **kwargs):
        """Function to load raw data from source, should be able to support 
        reading data from flat file or sql database. Please just implement the one using flat file now,
        later we would provide the sql python package that we would want to utilize for the database task
        
        Parameters:
            source_type: str
                flat file type or sql, if it is flat file, file directory or 
                path need to be passed in as argument or in the setup function
                If it is sql, connection need to be extablished in setup function
                please avoid any hard coded name in the class, and set global variable to define those file name
        """
        raise NotImplementedError("Subclasses should implement load_raw_data function!")
    
    def set_hyper_parameter(self, **kwargs):
        """Function to re_config any hyper parameters that you need for your model, 
        the parameters should be initialized in your inherited setup function, by reading the config
        either from a config file or from argument, but please enable user to have a config file to set
        these hyper-parameters."""
        raise NotImplementedError("Subclasses should implement set_hyper_parameter!")

    def print_hyper_parameter(self, **kwargs):
        """Print all the hyper parameters that you set for your model."""
        raise NotImplementedError("Subclasses should implement print_hyper_parameter!")
    
    def fit(self, **kwargs):
        """Function to execute training either based on the data that you load from file or passed in as argument.
        When X, Y are passed in as argument, would train the model based on the training dataset passed in, and over write
        the existing data cached in the strategy obj. If you implement some new machine learning model rather than using
        existing machine learning model by some python package, please seperate the implementation of the model in another class,
        and initialize an instance of that model in your setup function rather than implement the model directly in the fit function,
        so that we could seprate the business logics with the machine learning model maintaining logics, and those model could be reused
        somewhere else too."""
        raise NotImplementedError("Subclasses should implement print_hyper_parameter!")
    
    def predict(self, **kwargs):
        """Run prediction after fitting the model, should throw error message when the model did not run fit yet."""
        raise NotImplementedError("Subclasses should implement predict")
    
    def model_summary(self):
        """Function that provide summary of model result: prediction accuracy, different matrix 
            to measure the model, and hyper-parameters of the model"

        Parameters:
            None

            Return
                dict {str: float/dataframe}
                key is the staticial measure name
                value is the statical measure, either a number or a matrix or a dataframe
        """
        raise NotImplementedError("Subclasses should implement model_summary")

    def output_result(self, **kwargs):
        """Function to output the model, could use pickle to cached the obj that 
        has been trained, so that you could load the obj later directly later, and you could also use this function
        to output the optimal cluster, please use arguments to config what you want to output
        
        Parameters:
            output_model: bool
                output model to pickle container
            output_cluster: bool
                output cluster for each fund
        """
        raise NotImplementedError("Subclasses should implement output_result")
