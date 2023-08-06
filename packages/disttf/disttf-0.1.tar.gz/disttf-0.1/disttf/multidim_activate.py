import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K

import numpy as np


class ActivateLayer(keras.layers.Layer):
    """Gaussian Activation Layer"""
    def __init__(self):
        super(ActivateLayer, self).__init__()

    def build(self,input_shape):
        pass


    def call(self, inputs):
        q,v=inputs
        def gaussian(x):
            return K.exp(-K.sum(K.square(x),axis=-1)/2)/(np.sqrt(2*np.pi)**x.shape[-1])
        g=gaussian(q)
        return K.sum(g*v,axis=-1)
        
    def compute_output_shape(self, input_shape):
        qs,vs=input_shape
        return qs[:-1]









