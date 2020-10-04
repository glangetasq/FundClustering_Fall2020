# Base Logger Class

class BaseLogger:

    def __init__(self):
        pass


    def dump(self, title, **kwargs):

        print(f"Title: {title}")

        from key, value in kwargs.items():

            print(f"{key} : {value}")
