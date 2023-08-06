import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K


def determinant_regularizer(mult=1):
    def func(x):
        #return mult*(tf.linalg.det(x) - 1) ** 2
        return mult*K.mean(K.abs(tf.linalg.det(x) - 1))#+1000000.0
        return mult*K.sqrt(K.mean(K.abs(tf.linalg.det(x) - 1)**2))#+1000000.0
    return func

def identity_init(shape, dtype=None):
    return tf.repeat(K.reshape(tf.eye(shape[1], dtype=dtype),(1,shape[1],shape[1])),shape[0],axis=0)



class MixtureLayer(keras.layers.Layer):
    def __init__(self,reg=1.0):
        super(MixtureLayer, self).__init__()
        self.reg=reg

    def build(self,input_shape):
        qs,vs=input_shape
        self.mixture = self.add_weight("mixture",
                                  shape=(qs[1],qs[2],qs[2]),
                                  initializer=identity_init,#keras.initializers.Identity(gain=1.0),
                                  regularizer=determinant_regularizer(self.reg),
                                  trainable=True)
        #self.regularizer=lambda :determinant_regularizer(self.reg)(self.mixture)


    def call(self, inputs):
        q,v=inputs
        mix=self.mixture
        def one_func(q):
            return K.batch_dot(q,mix)
        q=K.map_fn(one_func,q)
        return q,v

    def compute_output_shape(self, input_shape):
        return input_shape









