import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K



class ScaleLayer(keras.layers.Layer):
    def __init__(self,epsilon=1e-6):
        super(ScaleLayer, self).__init__()
        self.epsilon=epsilon

    def build(self,input_shape):
        qs,vs=input_shape
        self.sigma = self.add_weight("sigma",
                                  shape=qs[1:],
                                  #initializer="truncated_normal",
                                  initializer="ones",
                                  trainable=True)


    def call(self, inputs):
        q,v=inputs
        sigma=K.abs(self.sigma)+self.epsilon
        return q/sigma,v/K.prod(sigma,axis=-1)

    def compute_output_shape(self, input_shape):
        return input_shape









