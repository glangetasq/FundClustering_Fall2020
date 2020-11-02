
import os
import pickle


def output_model(model, filename, loc=None):
    if not loc:
        loc = "OutputResults/OutputModels"

    with open(f'{loc}/{filename}.pickle', 'wb') as f:
        pickle.dump(model, f)
        print(f'Successfully saved the model to {loc}/{filename}.pickle!')
