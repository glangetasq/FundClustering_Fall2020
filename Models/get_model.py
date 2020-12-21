
from .Classic import TwoLayerFundClustering

ALL_MODELS = {
    'classic' : TwoLayerFundClustering
}


def get_model(model, *args, **kwargs):
    return ALL_MODELS[model.lower()](*args, **kwargs)
