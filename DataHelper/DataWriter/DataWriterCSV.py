

# Local Imports

from .BaseDataWriter import BaseDataWriter


class DataWriterCSV(BaseDataWriter):

    def update_raw_data(self, dataframe, path=None, **kwargs):
        """assuming that your data source is the csv file containing all the raw data, load the raw data from csv, and update the table
        which you already setup based on your template

        Careful! It replaces all current data in the table to the dataframe data

        Input:
            - dataframe: pd.DataFrame, dataframe with correct column names, and type
        """

        dataframe.to_csv(path, **kwargs)
