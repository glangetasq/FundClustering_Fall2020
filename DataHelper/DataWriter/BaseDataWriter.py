


class BaseDataWriter:

    def __init__(self):
        pass


    def update_raw_data(self):
        raise NotImplementedError("Children of BaseDataWriter should have update_raw_data implemented.")
