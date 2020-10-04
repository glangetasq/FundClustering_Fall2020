from sklearn.base import BaseEstimator, TransformerMixin

class TransformerBased(BaseEstimator, TransformerMixin):
    """Transformer based class to be define for each unsupervised learning processing, this define the
    required method that you need to define for the model in order to pass the model into the pipeline
    docs: 1) https://towardsdatascience.com/pipelines-custom-transformers-in-scikit-learn-the-step-by-step-guide-with-python-code-4a7d9b068156
          2) https://towardsdatascience.com/custom-transformers-and-ml-data-pipelines-with-python-20ea2a7adb65
    related reading: estimator
    docs: http://danielhnyk.cz/creating-your-own-estimator-scikit-learn/
    https://gist.github.com/amberjrivera/8c5c145516f5a2e894681e16a8095b5c
    """

    def __init__(self, **kwargs):
        """
        initialize the Estimator based on arguments
        """
        pass

    def fit(self, **kwargs):
        """
        Implement you model here for the estimators, please try to generate private method and modularize the model setup if
        the model is complicated

        """
        raise NotImplementedError("Subclasses should implement fit")

    def transform(self, **kwargs):
        raise NotImplementedError("Subclasses should implement predict")
