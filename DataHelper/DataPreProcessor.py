
class DataPreProcessor:
    """
    Class helping to preprocess the data.
    """

    @staticmethod
    def compute_cumulative_returns(returns):
        return (1+returns).cumprod()
