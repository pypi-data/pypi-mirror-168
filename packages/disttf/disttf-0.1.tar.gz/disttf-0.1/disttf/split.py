import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K



class SplitLayer(keras.layers.Layer):
    def __init__(self, num_splits):
        super(SplitLayer, self).__init__()
        self.num_splits = num_splits

    def build(self,input_shape):
        self.fact=self.add_weight(name='fact',shape=(self.num_splits,),initializer='ones',trainable=True)

    def call(self, inputs):
        q,v=inputs
        fact=self.fact
        fact=K.abs(fact)
        fact=fact/K.sum(fact)
        if len(q.shape)==2:
            q=tf.expand_dims(q, axis=1)

        #fact=tf.repeat(fact, q.shape[1])
        #print(v.shape,fact.shape)
        #v=v*fact
        #print(v.shape)
        #exit()
        fact=K.concatenate([fact]*q.shape[1],axis=0)#repeat(a,b) is a,a,a...b,b,b...this is a,b,a,b,a,b...
        return tf.repeat(q, self.num_splits, axis=1),fact*tf.repeat(v, self.num_splits, axis=0)#/self.num_splits

    def compute_output_shape(self, input_shape):
        input_shape=input_shape[0]
        if len(input_shape)==2:
            return (input_shape[0], self.num_splits, input_shape[1]), (self.num_splits)
        else:
            return (input_shape[0], self.num_splits*input_shape[1], input_shape[2]), (self.num_splits)*input_shape[1]









