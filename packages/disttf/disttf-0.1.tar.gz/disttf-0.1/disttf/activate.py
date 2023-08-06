import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K

import numpy as np


def gaussian(x):
    return K.exp(-K.square(x)/2)/(np.sqrt(2*np.pi))
class ActivateLayer(keras.layers.Layer):
    """Gaussian Activation Layer"""
    def __init__(self,func=gaussian):
        super(ActivateLayer, self).__init__()
        self.func=func

    def build(self,input_shape):
        pass


    def call(self, inputs):
        q,v=inputs
        g=self.func(q)
        g=K.prod(g,axis=-1)
        return K.sum(g*v,axis=-1)
        
    def compute_output_shape(self, input_shape):
        qs,vs=input_shape
        return qs[:-1]









