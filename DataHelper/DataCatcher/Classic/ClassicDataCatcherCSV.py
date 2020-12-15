
# Local imports
import DataHelper
from ..BaseCSVDataCatcher import BaseCSVDataCatcher
from Tools.latest_date_in_dataframe import latest_date_in_dataframe

class ClassicDataCatcherCSV(BaseCSVDataCatcher):

    __instance = None


    def __init__(self):
        raise RuntimeError('Call instance() instead')


    @classmethod
    def instance(cls, **kwargs):

        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            super(cls, cls.__instance).__init__(**kwargs)

        return cls.__instance
