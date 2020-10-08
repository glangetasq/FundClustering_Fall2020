
class DataPreProcessor:
    """
    Class helping to preprocess the data.
    """

    def __init__(self):
        pass

    @staticmethod
    def compute_cumulative_returns(returns):
        return (1+returns).cumprod()
