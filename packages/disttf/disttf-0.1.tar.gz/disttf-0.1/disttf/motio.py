import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K



class MotioLayer(keras.layers.Layer):
    def __init__(self):
        super(MotioLayer, self).__init__()

    def build(self,input_shape):
        qs,vs=input_shape
        self.mu = self.add_weight("mu",
                                  shape=qs[1:],
                                  initializer="truncated_normal",
                                  trainable=True)


    def call(self, inputs):
        q,v=inputs
        return q+self.mu,v

    def compute_output_shape(self, input_shape):
        return input_shape









