
import os
import pickle


def save_model(sv_mdl, path, model):

    if sv_mdl:
        if path:
            pickle.dump(model, path)
        else:
            raise ValueError("Should define path when trying to save model to pickle.")
