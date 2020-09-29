from sklearn.base import BaseEstimator

class EstimatorBased(BaseEstimator):
    """Estimator based class to be define for each clustering layer,
    this define the required method that you need to define for the
    model in order to pass the model into the pipeline docs: https://scikit-learn.org/stable/developers/develop.html """

    def __init__(self, **kwargs):
        """
        initialize the Estimator based on arguments
        """
        pass

    def fit(self, **kwargs):
        """
        Implement you model here for the estimators, please try to generate private method and modularize the model setup if
        the model is complicate

        """
        raise NotImplementedError("Subclasses should implement fit")

    def predict(self, **kwargs):
        raise NotImplementedError("Subclasses should implement predict")


