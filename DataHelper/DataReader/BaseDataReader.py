

class BaseDataReader:

    def __init__(self, reader_type=None):
        self.reader_type = reader_type
        self.dataframes = dict()


    def is_reader_type(self, reader_type):
        return self.reader_type == reader_type.lower()


    @staticmethod
    def get_returns():
        raise NotImplementedError("DataReader subclasses should implement get_returns")


    @staticmethod
    def get_holding_asset():
        raise NotImplementedError("DataReader subclasses should implement get_holding_asset")


    @staticmethod
    def get_fund_mrnstar():
        raise NotImplementedError("DataReader subclasses should implement get_fund_mrnstar")


    @staticmethod
    def get_fundno_ticker():
        raise NotImplementedError("DataReader subclasses should implement get_fundno_ticker")
