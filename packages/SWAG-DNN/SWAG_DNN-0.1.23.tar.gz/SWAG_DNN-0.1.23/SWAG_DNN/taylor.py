

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import matplotlib.pyplot as plt 

from keras.optimizers import Optimizer
# from keras.legacy import interfaces
from keras import backend as K
from keras.utils.generic_utils import get_custom_objects
import timeit
import numpy as np
import pandas as pd
from keras.models import Sequential
from sklearn.model_selection import KFold,train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from pandas import read_csv
from keras.datasets import mnist
from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
from keras.models import Sequential
from keras.initializers import RandomNormal,glorot_normal
from sklearn.model_selection import StratifiedKFold
from keras.utils.vis_utils import plot_model

from keras import backend as K
from keras import initializers,regularizers,constraints
from tensorflow.keras import layers
from keras.initializers import RandomNormal,glorot_normal
from keras.layers import Input, Embedding, Dense,concatenate,InputSpec
from keras.layers import  Activation,concatenate,InputSpec
from keras.utils import conv_utils,np_utils 
from keras.utils.generic_utils import deserialize_keras_object,has_arg,get_custom_objects
from keras.utils.generic_utils import deserialize_keras_object
np.random.seed(7)
from keras import activations
import tensorflow as tf

p1=1
p2=2
p3=6
p4=24
p5=120
p6=720
p7=1

def create_model_classic(active1,active2):
    # create model
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation=active1))
    model.add(Dense(12, activation=active2))
    model.add(Dense(20))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

"""### To Run the code you need to download this file. it is the implementation of SWAG Layer.

### Define a set of custom activation functions. We will define $X,X^2,X^3,X^4,X^5,X^6,X^7,X^8$
"""

#Defining New Activation functions
############################################################################
def X_1(x):
    return (K.pow(x,1))
get_custom_objects().update({'X_1': Activation(X_1)})
############################################################################
def X_2(x):
    return (K.pow(x,2))/2
get_custom_objects().update({'X_2': Activation(X_2)})
############################################################################
def X_3(x):
    return (K.pow(x,3))/6
get_custom_objects().update({'X_3': Activation(X_3)})
############################################################################
def X_4(x):
    return (K.pow(x,4))/24
get_custom_objects().update({'X_4': Activation(X_4)})
############################################################################
def X_5(x):
    return (K.pow(x,5))/120
get_custom_objects().update({'X_5': Activation(X_5)})
###############################################################################
def X_6(x):
    return (K.pow(x,6))/720
get_custom_objects().update({'X_6': Activation(X_6)})

#Defining New Activation functions
############################################################################
def S_X_1(x):
    return (K.sin(x))
get_custom_objects().update({'S_X_1': Activation(S_X_1)})
############################################################################
def S_X_2(x):
    return (K.sin(2*x))
get_custom_objects().update({'S_X_2': Activation(S_X_2)})
############################################################################
def S_X_3(x):
    return (K.sin(3*x))
get_custom_objects().update({'S_X_3': Activation(S_X_3)})
############################################################################
def S_X_4(x):
    return (K.sin(4*x))
get_custom_objects().update({'S_X_4': Activation(S_X_4)})
############################################################################
def S_X_5(x):
    return (K.sin(5*x))
get_custom_objects().update({'S_X_5': Activation(S_X_5)})
###############################################################################
def S_X_6(x):
    return (K.sin(6*x))
get_custom_objects().update({'S_X_6': Activation(S_X_6)})
###############################################################################

#Defining New Activation functions
############################################################################
def C_a_X_1(x):
    return (K.pow(x,1))/p1
get_custom_objects().update({'C_a_X_1': Activation(C_a_X_1)})
############################################################################
def C_a_X_2(x):
    return ((2*K.pow(x,2))-1)/p2
get_custom_objects().update({'C_a_X_2': Activation(C_a_X_2)})
############################################################################
def C_a_X_3(x):
    return ((4*K.pow(x,3))-(3*x))/p3
get_custom_objects().update({'C_a_X_3': Activation(C_a_X_3)})
############################################################################
def C_a_X_4(x):
    return ((8*K.pow(x,4))-(8*K.pow(x,2))+1)/p4
get_custom_objects().update({'C_a_X_4': Activation(C_a_X_4)})
############################################################################
def C_a_X_5(x):
    return ((16*K.pow(x,5))-(20*K.pow(x,3))+(5*x))/p5
get_custom_objects().update({'C_a_X_5': Activation(C_a_X_5)})
############################################################################
def C_a_X_6(x):
    return ((32*K.pow(x,6))-(48*K.pow(x,4))+(18*K.pow(x,2))-1)/p6
get_custom_objects().update({'C_a_X_6': Activation(C_a_X_6)})

#Defining New Activation functions
############################################################################
def C_b_X_1(x):
    return (2*K.pow(x,1))/p1
get_custom_objects().update({'C_b_X_1': Activation(C_b_X_1)})
############################################################################
def C_b_X_2(x):
    return ((4*K.pow(x,2))-1)/p2
get_custom_objects().update({'C_b_X_2': Activation(C_b_X_2)})
############################################################################
def C_b_X_3(x):
    return ((8*K.pow(x,3))-(4*x))/p3
get_custom_objects().update({'C_b_X_3': Activation(C_b_X_3)})
############################################################################
def C_b_X_4(x):
    return ((16*K.pow(x,4))-(12*K.pow(x,2))+1)/p4
get_custom_objects().update({'C_b_X_4': Activation(C_b_X_4)})
############################################################################
def C_b_X_5(x):
    return ((32*K.pow(x,5))-(32*K.pow(x,3))+6*x)/p5
get_custom_objects().update({'C_b_X_5': Activation(C_b_X_5)})
############################################################################
def C_b_X_6(x):
    return ((64*K.pow(x,4))-(80*K.pow(x,4))+(24*K.pow(x,2))-1)/p6
get_custom_objects().update({'C_b_X_6': Activation(C_b_X_6)})

#Defining New Activation functions
############################################################################
def H_X_1(x):
    return (2*K.pow(x,1))/p1
get_custom_objects().update({'H_X_1': Activation(H_X_1)})
############################################################################
def H_X_2(x):
    return ((4*K.pow(x,2))-2)/p2
get_custom_objects().update({'H_X_2': Activation(H_X_2)})
############################################################################
def H_X_3(x):
    return ((8*K.pow(x,3))-(12*x))/p3
get_custom_objects().update({'H_X_3': Activation(H_X_3)})
############################################################################
def H_X_4(x):
    return ((16*K.pow(x,4))-(48*K.pow(x,2))+12)/p4
get_custom_objects().update({'H_X_4': Activation(H_X_4)})
############################################################################
def H_X_5(x):
    return ((32*K.pow(x,5))-(160*K.pow(x,3))+120*x)/p5
get_custom_objects().update({'H_X_5': Activation(H_X_5)})
############################################################################
def H_X_6(x):
    return ((64*K.pow(x,6))-(480*K.pow(x,4))+(720*K.pow(x,2))-120)/p6
get_custom_objects().update({'H_X_6': Activation(H_X_6)})

#Defining New Activation functions
############################################################################
def L_X_1(x):
    return (K.pow(x,1))/p1
get_custom_objects().update({'L_X_1': Activation(L_X_1)})
############################################################################
def L_X_2(x):
    return ((3*K.pow(x,2))-1)/(2*p2)
get_custom_objects().update({'L_X_2': Activation(L_X_2)})
############################################################################
def L_X_3(x):
    return ((5*K.pow(x,3))-(3*x))/(2*p3)
get_custom_objects().update({'L_X_3': Activation(L_X_3)})
############################################################################
def L_X_4(x):
    return ((35*K.pow(x,4))-(32*K.pow(x,2))+3)/(8*p4)
get_custom_objects().update({'L_X_4': Activation(L_X_4)})
############################################################################
def L_X_5(x):
    return ((63*K.pow(x,5))-(70*K.pow(x,3))+15*x)/(8*p5)
get_custom_objects().update({'L_X_5': Activation(L_X_5)})
############################################################################
def L_X_6(x):
    return  ((231*K.pow(x,6))-(315*K.pow(x,4))+(105*K.pow(x,2))-5)/(16*p6)
get_custom_objects().update({'L_X_6': Activation(L_X_6)})

"""### Dense_Co is a custom Keras Layer which we develop to implement SWAG

"""

class Dense_Ch_a(tf.keras.layers.Layer):
    def __init__(self, units,
                 activation=None,
                 hidden_dim=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(Dense_Ch_a, self).__init__(**kwargs)
        self.units = units
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)
        self.input_spec = InputSpec(min_ndim=2)
        self.supports_masking = True
        if hidden_dim!=None :
            self.hidden_dim = hidden_dim
        else :
            self.hidden_dim=self.units
                

    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[-1]     
##########################################################################      
        self.kernel1 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel2 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel3 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel4 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel5 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel6 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
    
    


    
    
    
##########################################################################
        self.kernel_all = self.add_weight(shape=(6*self.hidden_dim, self.units),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
##########################################################################    
        if self.use_bias:
            self.bias1 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias2 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias3 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias4 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
            self.bias5 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias6 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)                        
            
###########################################################################
            self.bias_all = self.add_weight(shape=(self.units,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
    
        else:
            self.bias = None
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True

    def call(self, inputs):
        output1 = K.dot(inputs, self.kernel1)
        output2 = K.dot(inputs, self.kernel2) 
        output3 = K.dot(inputs, self.kernel3)
        output4 = K.dot(inputs, self.kernel4)
        output5 = K.dot(inputs, self.kernel5) 
        output6 = K.dot(inputs, self.kernel6)
 
        if self.use_bias:
            output1 = K.bias_add(output1, self.bias1, data_format='channels_last')
            output2 = K.bias_add(output2, self.bias2, data_format='channels_last')
            output3 = K.bias_add(output3, self.bias3, data_format='channels_last')
            output4 = K.bias_add(output4, self.bias4, data_format='channels_last')
            output5 = K.bias_add(output5, self.bias5, data_format='channels_last')
            output6 = K.bias_add(output6, self.bias6, data_format='channels_last')
            
        self.activation= activations.get('C_a_X_1')
        output1 = self.activation(output1)

        self.activation= activations.get('C_a_X_2')
        output2 = self.activation(output2)

        self.activation= activations.get('C_a_X_3')            
        output3 = self.activation(output3) 

        self.activation= activations.get('C_a_X_4')
        output4 = self.activation(output4)

        self.activation= activations.get('C_a_X_5')
        output5 = self.activation(output5)

        self.activation= activations.get('C_a_X_6')            
        output6 = self.activation(output6) 
        output_all=concatenate([output1,output2,output3,output4,output5,output6])

        output_all = K.dot(output_all, self.kernel_all)  
        output_all = K.bias_add(output_all, self.bias_all, data_format='channels_last')
        self.activation= activations.get('linear')
        output_all = self.activation(output_all)
            
        return output_all

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.units
        return tuple(output_shape)

    def get_config(self):
        config = {
            'units': self.units,
            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
            'bias_initializer': initializers.serialize(self.bias_initializer),
            'kernel_regularizer': regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': regularizers.serialize(self.bias_regularizer),
            'activity_regularizer':
                regularizers.serialize(self.activity_regularizer),
            'kernel_constraint': constraints.serialize(self.kernel_constraint),
            'bias_constraint': constraints.serialize(self.bias_constraint)
        }
        base_config = super(Dense, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class Dense_Ch_b(tf.keras.layers.Layer):
    def __init__(self, units,
                 activation=None,
                 hidden_dim=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(Dense_Ch_b, self).__init__(**kwargs)
        self.units = units
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)
        self.input_spec = InputSpec(min_ndim=2)
        self.supports_masking = True
        if hidden_dim!=None :
            self.hidden_dim = hidden_dim
        else :
            self.hidden_dim=self.units
                

    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[-1]     
##########################################################################      
##########################################################################      
        self.kernel1 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel2 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel3 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel4 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel5 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel6 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
    
    


    
    
    
##########################################################################
        self.kernel_all = self.add_weight(shape=(6*self.hidden_dim, self.units),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
##########################################################################    
        if self.use_bias:
            self.bias1 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias2 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias3 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias4 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
            self.bias5 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias6 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)                        
            
###########################################################################
            self.bias_all = self.add_weight(shape=(self.units,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

        else:
            self.bias = None
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True

    def call(self, inputs):
        output1 = K.dot(inputs, self.kernel1)
        output2 = K.dot(inputs, self.kernel2) 
        output3 = K.dot(inputs, self.kernel3)
        output4 = K.dot(inputs, self.kernel4)
        output5 = K.dot(inputs, self.kernel5) 
        output6 = K.dot(inputs, self.kernel6)
 
        if self.use_bias:
            output1 = K.bias_add(output1, self.bias1, data_format='channels_last')
            output2 = K.bias_add(output2, self.bias2, data_format='channels_last')
            output3 = K.bias_add(output3, self.bias3, data_format='channels_last')
            output4 = K.bias_add(output4, self.bias4, data_format='channels_last')
            output5 = K.bias_add(output5, self.bias5, data_format='channels_last')
            output6 = K.bias_add(output6, self.bias6, data_format='channels_last')
            
        self.activation= activations.get('C_b_X_1')
        output1 = self.activation(output1)

        self.activation= activations.get('C_b_X_2')
        output2 = self.activation(output2)

        self.activation= activations.get('C_b_X_3')            
        output3 = self.activation(output3) 

        self.activation= activations.get('C_b_X_4')
        output4 = self.activation(output4)

        self.activation= activations.get('C_b_X_5')
        output5 = self.activation(output5)

        self.activation= activations.get('C_b_X_6')            
        output6 = self.activation(output6) 
        output_all=concatenate([output1,output2,output3,output4,output5,output6])

        output_all = K.dot(output_all, self.kernel_all)  
        output_all = K.bias_add(output_all, self.bias_all, data_format='channels_last')
        self.activation= activations.get('linear')
        output_all = self.activation(output_all)
            
        return output_all

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.units
        return tuple(output_shape)

    def get_config(self):
        config = {
            'units': self.units,
            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
            'bias_initializer': initializers.serialize(self.bias_initializer),
            'kernel_regularizer': regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': regularizers.serialize(self.bias_regularizer),
            'activity_regularizer':
                regularizers.serialize(self.activity_regularizer),
            'kernel_constraint': constraints.serialize(self.kernel_constraint),
            'bias_constraint': constraints.serialize(self.bias_constraint)
        }
        base_config = super(Dense, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class Dense_S(tf.keras.layers.Layer):
    def __init__(self, units,
                 activation=None,
                 hidden_dim=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(Dense_S, self).__init__(**kwargs)
        self.units = units
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)
        self.input_spec = InputSpec(min_ndim=2)
        self.supports_masking = True
        if hidden_dim!=None :
            self.hidden_dim = hidden_dim
        else :
            self.hidden_dim=self.units
                

    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[-1]   


##########################################################################      
##########################################################################      
        self.kernel1 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel2 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel3 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel4 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel5 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel6 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
    
    


    
    
    
##########################################################################
        self.kernel_all = self.add_weight(shape=(6*self.hidden_dim, self.units),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
##########################################################################    
        if self.use_bias:
            self.bias1 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias2 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias3 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias4 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
            self.bias5 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias6 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)                        
            
###########################################################################
            self.bias_all = self.add_weight(shape=(self.units,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)


        else:
            self.bias = None
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True

    def call(self, inputs):
        output1 = K.dot(inputs, self.kernel1)
        output2 = K.dot(inputs, self.kernel2) 
        output3 = K.dot(inputs, self.kernel3)
        output4 = K.dot(inputs, self.kernel4)
        output5 = K.dot(inputs, self.kernel5) 
        output6 = K.dot(inputs, self.kernel6)
 
        if self.use_bias:
            output1 = K.bias_add(output1, self.bias1, data_format='channels_last')
            output2 = K.bias_add(output2, self.bias2, data_format='channels_last')
            output3 = K.bias_add(output3, self.bias3, data_format='channels_last')
            output4 = K.bias_add(output4, self.bias4, data_format='channels_last')
            output5 = K.bias_add(output5, self.bias5, data_format='channels_last')
            output6 = K.bias_add(output6, self.bias6, data_format='channels_last')
            
        self.activation= activations.get('S_X_1')
        output1 = self.activation(output1)

        self.activation= activations.get('S_X_2')
        output2 = self.activation(output2)

        self.activation= activations.get('S_X_3')            
        output3 = self.activation(output3) 

        self.activation= activations.get('S_X_4')
        output4 = self.activation(output4)

        self.activation= activations.get('S_X_5')
        output5 = self.activation(output5)

        self.activation= activations.get('S_X_6')            
        output6 = self.activation(output6) 
        output_all=concatenate([output1,output2,output3,output4,output5,output6])

        output_all = K.dot(output_all, self.kernel_all)  
        output_all = K.bias_add(output_all, self.bias_all, data_format='channels_last')
        self.activation= activations.get('linear')
        output_all = self.activation(output_all)
            
        return output_all

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.units
        return tuple(output_shape)

    def get_config(self):
        config = {
            'units': self.units,
            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
            'bias_initializer': initializers.serialize(self.bias_initializer),
            'kernel_regularizer': regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': regularizers.serialize(self.bias_regularizer),
            'activity_regularizer':
                regularizers.serialize(self.activity_regularizer),
            'kernel_constraint': constraints.serialize(self.kernel_constraint),
            'bias_constraint': constraints.serialize(self.bias_constraint)
        }
        base_config = super(Dense, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class Dense_H(tf.keras.layers.Layer):
    def __init__(self, units,
                 activation=None,
                 hidden_dim=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(Dense_H, self).__init__(**kwargs)
        self.units = units
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)
        self.input_spec = InputSpec(min_ndim=2)
        self.supports_masking = True
        if hidden_dim!=None :
            self.hidden_dim = hidden_dim
        else :
            self.hidden_dim=self.units
                

    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[-1]     
##########################################################################      
##########################################################################      
        self.kernel1 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel2 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel3 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel4 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel5 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel6 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
    
    


    
    
    
##########################################################################
        self.kernel_all = self.add_weight(shape=(6*self.hidden_dim, self.units),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
##########################################################################    
        if self.use_bias:
            self.bias1 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias2 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias3 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias4 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
            self.bias5 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias6 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)                        
            
###########################################################################
            self.bias_all = self.add_weight(shape=(self.units,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
    
        else:
            self.bias = None
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True

    def call(self, inputs):
        output1 = K.dot(inputs, self.kernel1)
        output2 = K.dot(inputs, self.kernel2) 
        output3 = K.dot(inputs, self.kernel3)
        output4 = K.dot(inputs, self.kernel4)
        output5 = K.dot(inputs, self.kernel5) 
        output6 = K.dot(inputs, self.kernel6)
 
        if self.use_bias:
            output1 = K.bias_add(output1, self.bias1, data_format='channels_last')
            output2 = K.bias_add(output2, self.bias2, data_format='channels_last')
            output3 = K.bias_add(output3, self.bias3, data_format='channels_last')
            output4 = K.bias_add(output4, self.bias4, data_format='channels_last')
            output5 = K.bias_add(output5, self.bias5, data_format='channels_last')
            output6 = K.bias_add(output6, self.bias6, data_format='channels_last')
            
        self.activation= activations.get('H_X_1')
        output1 = self.activation(output1)

        self.activation= activations.get('H_X_2')
        output2 = self.activation(output2)

        self.activation= activations.get('H_X_3')            
        output3 = self.activation(output3) 

        self.activation= activations.get('H_X_4')
        output4 = self.activation(output4)

        self.activation= activations.get('H_X_5')
        output5 = self.activation(output5)

        self.activation= activations.get('H_X_6')            
        output6 = self.activation(output6) 
        output_all=concatenate([output1,output2,output3,output4,output5,output6])

        output_all = K.dot(output_all, self.kernel_all)  
        output_all = K.bias_add(output_all, self.bias_all, data_format='channels_last')
        self.activation= activations.get('linear')
        output_all = self.activation(output_all)
            
        return output_all

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.units
        return tuple(output_shape)

    def get_config(self):
        config = {
            'units': self.units,
            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
            'bias_initializer': initializers.serialize(self.bias_initializer),
            'kernel_regularizer': regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': regularizers.serialize(self.bias_regularizer),
            'activity_regularizer':
                regularizers.serialize(self.activity_regularizer),
            'kernel_constraint': constraints.serialize(self.kernel_constraint),
            'bias_constraint': constraints.serialize(self.bias_constraint)
        }
        base_config = super(Dense, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class Dense_L(tf.keras.layers.Layer):
    def __init__(self, units,
                 activation=None,
                 hidden_dim=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(Dense_L, self).__init__(**kwargs)
        self.units = units
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)
        self.input_spec = InputSpec(min_ndim=2)
        self.supports_masking = True
        if hidden_dim!=None :
            self.hidden_dim = hidden_dim
        else :
            self.hidden_dim=self.units
                

    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[-1]     
##########################################################################      
##########################################################################      
        self.kernel1 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel2 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel3 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel4 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel5 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel6 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
    
    


    
    
    
##########################################################################
        self.kernel_all = self.add_weight(shape=(6*self.hidden_dim, self.units),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
##########################################################################    
        if self.use_bias:
            self.bias1 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias2 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias3 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias4 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
            self.bias5 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias6 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)                        
            
###########################################################################
            self.bias_all = self.add_weight(shape=(self.units,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
    
        else:
            self.bias = None
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True

    def call(self, inputs):
        output1 = K.dot(inputs, self.kernel1)
        output2 = K.dot(inputs, self.kernel2) 
        output3 = K.dot(inputs, self.kernel3)
        output4 = K.dot(inputs, self.kernel4)
        output5 = K.dot(inputs, self.kernel5) 
        output6 = K.dot(inputs, self.kernel6)
 
        if self.use_bias:
            output1 = K.bias_add(output1, self.bias1, data_format='channels_last')
            output2 = K.bias_add(output2, self.bias2, data_format='channels_last')
            output3 = K.bias_add(output3, self.bias3, data_format='channels_last')
            output4 = K.bias_add(output4, self.bias4, data_format='channels_last')
            output5 = K.bias_add(output5, self.bias5, data_format='channels_last')
            output6 = K.bias_add(output6, self.bias6, data_format='channels_last')
            
        self.activation= activations.get('L_X_1')
        output1 = self.activation(output1)

        self.activation= activations.get('L_X_2')
        output2 = self.activation(output2)

        self.activation= activations.get('L_X_3')            
        output3 = self.activation(output3) 

        self.activation= activations.get('L_X_4')
        output4 = self.activation(output4)

        self.activation= activations.get('L_X_5')
        output5 = self.activation(output5)

        self.activation= activations.get('L_X_6')            
        output6 = self.activation(output6) 
        output_all=concatenate([output1,output2,output3,output4,output5,output6])

        output_all = K.dot(output_all, self.kernel_all)  
        output_all = K.bias_add(output_all, self.bias_all, data_format='channels_last')
        self.activation= activations.get('linear')
        output_all = self.activation(output_all)
            
        return output_all

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.units
        return tuple(output_shape)

    def get_config(self):
        config = {
            'units': self.units,
            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
            'bias_initializer': initializers.serialize(self.bias_initializer),
            'kernel_regularizer': regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': regularizers.serialize(self.bias_regularizer),
            'activity_regularizer':
                regularizers.serialize(self.activity_regularizer),
            'kernel_constraint': constraints.serialize(self.kernel_constraint),
            'bias_constraint': constraints.serialize(self.bias_constraint)
        }
        base_config = super(Dense, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class Dense_Co(tf.keras.layers.Layer):
    def __init__(self, units,
                 activation=None,
                 hidden_dim=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(Dense_Co, self).__init__(**kwargs)
        self.units = units
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)
        self.input_spec = InputSpec(min_ndim=2)
        self.supports_masking = True
        if hidden_dim!=None :
            self.hidden_dim = hidden_dim
        else :
            self.hidden_dim=self.units
                

    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[-1]     
##########################################################################      
##########################################################################      
        self.kernel1 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel2 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel3 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel4 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.kernel5 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        
        self.kernel6 = self.add_weight(shape=(input_dim, self.hidden_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
    
    


    
    
    
##########################################################################
        self.kernel_all = self.add_weight(shape=(6*self.hidden_dim, self.units),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
##########################################################################    
        if self.use_bias:
            self.bias1 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias2 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias3 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias4 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
            self.bias5 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

            self.bias6 = self.add_weight(shape=(self.hidden_dim,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)                        
            
###########################################################################
            self.bias_all = self.add_weight(shape=(self.units,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
    
        else:
            self.bias = None
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True

    def call(self, inputs):
        output1 = K.dot(inputs, self.kernel1)
        output2 = K.dot(inputs, self.kernel2) 
        output3 = K.dot(inputs, self.kernel3)
        output4 = K.dot(inputs, self.kernel4)
        output5 = K.dot(inputs, self.kernel5) 
        output6 = K.dot(inputs, self.kernel6)
 
        if self.use_bias:
            output1 = K.bias_add(output1, self.bias1, data_format='channels_last')
            output2 = K.bias_add(output2, self.bias2, data_format='channels_last')
            output3 = K.bias_add(output3, self.bias3, data_format='channels_last')
            output4 = K.bias_add(output4, self.bias4, data_format='channels_last')
            output5 = K.bias_add(output5, self.bias5, data_format='channels_last')
            output6 = K.bias_add(output6, self.bias6, data_format='channels_last')
            
        self.activation= activations.get('X_1')
        output1 = self.activation(output1)

        self.activation= activations.get('X_2')
        output2 = self.activation(output2)

        self.activation= activations.get('X_3')            
        output3 = self.activation(output3) 

        self.activation= activations.get('X_4')
        output4 = self.activation(output4)

        self.activation= activations.get('X_5')
        output5 = self.activation(output5)

        self.activation= activations.get('X_6')            
        output6 = self.activation(output6) 
        output_all=concatenate([output1,output2,output3,output4,output5,output6])

        output_all = K.dot(output_all, self.kernel_all)  
        output_all = K.bias_add(output_all, self.bias_all, data_format='channels_last')
        self.activation= activations.get('linear')
        output_all = self.activation(output_all)
            
        return output_all

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.units
        return tuple(output_shape)

    def get_config(self):
        config = {
            'units': self.units,
            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
            'bias_initializer': initializers.serialize(self.bias_initializer),
            'kernel_regularizer': regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': regularizers.serialize(self.bias_regularizer),
            'activity_regularizer':
                regularizers.serialize(self.activity_regularizer),
            'kernel_constraint': constraints.serialize(self.kernel_constraint),
            'bias_constraint': constraints.serialize(self.bias_constraint)
        }
        base_config = super(Dense, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

"""### Define normalize Functions

### Define Rescaling Functions from 0-1 to 0.1-0.9

"""

#Define normalize Functions
def normalize(d):
    # d is a (n x dimension) np array
    d -= np.min(d, axis=0)
    d /= np.ptp(d, axis=0)
    return d

#Define Rescaling Functions from 0-1 to 0.1-0.9
def rescale_range(d):
    # d is a (n x dimension) np array
    d=np.multiply(d, 0.89)
    d=np.add(d, 0.01)
    return d

"""### This method compiles a Keras model and return it.
### input_dim is the dimension of input and  output_dim is the dimension of output.
### In our model image the number of Green, Red, and Blue are equal, and we show them by hidden_dim
### by default hidden_dim = input_dim but we can change it.
"""

def build_model_v1(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_Co(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model


def SWAG(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_Co(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Ch_First(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_Ch_a(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Ch_second(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_Ch_b(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Hermite(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_H(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Legendre(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_L(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Sin(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_S(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model



def build_model_v1(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_Co(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model


def SWAG(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_Co(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Ch_First__(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_Ch_a(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Ch_second__(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_Ch_b(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Hermite__(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_H(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Legendre__(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_L(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

def Sin__(input_dim,hidden_dim,output_dim):
    model = Sequential()
    model.add(Dense_S(output_dim,hidden_dim=hidden_dim ,input_dim=input_dim,  kernel_initializer=RandomNormal(
            mean=0.0, stddev=0.04), bias_initializer=RandomNormal(mean=0.0, stddev=0.04)))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model

