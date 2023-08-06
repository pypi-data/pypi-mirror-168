import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K

import numpy as np


class AsymActivateLayer(keras.layers.Layer):
    """Gaussian Activation Layer"""
    def __init__(self):
        super(AsymActivateLayer, self).__init__()

    def build(self,input_shape):
        qs,vs=input_shape
        self.gamma=self.add_weight(name='gamma',shape=qs[1:],trainable=True)


    def call(self, inputs):
        q,v=inputs

        def theta(x):
            return (K.sign(x)+1)/2

        def asym(x,gamma):
            e1=K.exp(-x**2/2)
            e2=K.exp(-x**2/(2*gamma**2))
            e=(1-theta(x))*e1+theta(x)*e2
            e*=(2/(np.sqrt(2*np.pi)*(1+gamma)))
            return e





        g=asym(q,K.abs(self.gamma))
        g=K.prod(g,axis=-1)
        return K.sum(g*v,axis=-1)
        
    def compute_output_shape(self, input_shape):
        qs,vs=input_shape
        return qs[:-1]









