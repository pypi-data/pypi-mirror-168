import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K

import numpy as np


class BoxyActivateLayer(keras.layers.Layer):
    """Gaussian Activation Layer"""
    def __init__(self):
        super(BoxyActivateLayer, self).__init__()

    def build(self,input_shape):
        qs,vs=input_shape
        self.gamma=self.add_weight(name='gamma',shape=qs[1:],trainable=True)


    def call(self, inputs):
        q,v=inputs

        def boxy(x,gamma):
            e1=K.exp(gamma*(1+x))
            e2=K.exp(gamma*(1-x))
            e1=K.expand_dims(e1,axis=-1)
            e2=K.expand_dims(e2,axis=-1)
            c=K.ones_like(e1)
            c=K.concatenate([c,e1,e2],axis=-1)
            c=K.min(c,axis=-1)
            q=gamma/(2+2*gamma)
            return q*c




        g=boxy(q,K.abs(self.gamma))
        g=K.prod(g,axis=-1)
        return K.sum(g*v,axis=-1)
        
    def compute_output_shape(self, input_shape):
        qs,vs=input_shape
        return qs[:-1]









