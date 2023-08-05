# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 12:06:26 2022

@author: vip
"""

import tensorflow as tf
from keras import backend as K
from keras.models import Sequential, Model,load_model
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.layers import Dropout, Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D,MaxPool2D
from keras.preprocessing import image
from keras.initializers import glorot_uniform

class identity_block(tf.keras.layers.Layer):
    def __init__(self, f, filters, stage, block):
        super(identity_block, self).__init__()
        
        self.conv_name_base = 'res' + str(stage) + block + '_branch'
        self.bn_name_base = 'bn' + str(stage) + block + '_branch'
        self.F1, self.F2, self.F3 = filters
       
        
        self.conv1 = Conv2D(filters=self.F1, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=self.conv_name_base + '2a', kernel_initializer=glorot_uniform(seed=0))
        self.bn1 = BatchNormalization(axis=3, name=self.bn_name_base + '2a')
        self.act1 = Activation('relu')
        
        self.conv2 = Conv2D(filters=self.F2, kernel_size=(f, f), strides=(1, 1), padding='same', name=self.conv_name_base + '2b', kernel_initializer=glorot_uniform(seed=0))
        self.bn2 = BatchNormalization(axis=3, name=self.bn_name_base + '2b')
        self.act2 = Activation('relu')
        
        self.conv3 = Conv2D(filters=self.F3, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=self.conv_name_base + '2c', kernel_initializer=glorot_uniform(seed=0))
        self.bn3 = BatchNormalization(axis=3, name=self.bn_name_base + '2c')
        
        self.act4 = Activation('relu')
        
    def call(self,inputs):
        
        conv_name = self.conv_name_base
        bn_name = self.bn_name_base
        F1,F2,F3 = self.F1, self.F2, self.F3
        X_shortcut = inputs
        
        x = self.conv1(X_shortcut)
        x = self.bn1(x)
        x = self.act1(x)
        
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.act2(x)
        
        x = self.conv3(x)
        x = self.bn3(x)
        
        x = Add()([x, X_shortcut])
        x = self.act4(x)
        
        return x


class convolutional_block(tf.keras.layers.Layer):
    def __init__(self, f, filters, stage, block , s=2):
        super(convolutional_block, self).__init__()
        
        self.conv_name_base = 'res' + str(stage) + block + '_branch'
        self.bn_name_base = 'bn' + str(stage) + block + '_branch'
        self.F1, self.F2, self.F3 = filters
       
        
        self.con1 = Conv2D(filters= self.F1, kernel_size=(1, 1), strides=(s, s), padding='valid', name=self.conv_name_base + '2a', kernel_initializer=glorot_uniform(seed=0))
        self.bno1 = BatchNormalization(axis=3, name=self.bn_name_base + '2a')
        self.acti1 = Activation('relu')
        
        self.con2 = Conv2D(filters=self.F2, kernel_size=(f, f), strides=(1, 1), padding='same', name=self.conv_name_base + '2b', kernel_initializer=glorot_uniform(seed=0))
        self.bno2 = BatchNormalization(axis=3, name=self.bn_name_base + '2b')
        self.acti2 = Activation('relu')
        
        self.con3 = Conv2D(filters=self.F3, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=self.conv_name_base + '2c', kernel_initializer=glorot_uniform(seed=0))
        self.bno3 = BatchNormalization(axis=3, name=self.bn_name_base + '2c')
        
        self.coni4 = Conv2D(filters=self.F3, kernel_size=(1, 1), strides=(s, s), padding='valid', name=self.conv_name_base + '1', kernel_initializer=glorot_uniform(seed=0))
        self.bno4 = BatchNormalization(axis=3, name=self.bn_name_base + '1')
        
      
        self.acti4 = Activation('relu')
    
    def call(self,inputs):
        
        conv_name = self.conv_name_base
        bn_name = self.bn_name_base
        F1,F2,F3 = self.F1, self.F2, self.F3
        X_shortcut = inputs
        
        x = self.con1(inputs)
        x = self.bno1(x)
        x = self.acti1(x)
        
        x = self.con2(x)
        x = self.bno2(x)
        x = self.acti2(x)
        
        x = self.con3(x)
        x = self.bno3(x)
        
        X_shortcut = self.coni4(X_shortcut)
        X_shortcut = self.bno4(X_shortcut)
        
        x = Add()([x,X_shortcut])
        x = self.acti4(x)
        
        return x


class ResNet50(tf.keras.Model):
    def __init__(self , num_classes):
        super(ResNet50, self).__init__()
        
        self.num_classes = num_classes
        
        self.zeropadding = ZeroPadding2D((3, 3))
        self.conn = Conv2D(64, (7, 7), strides=(2, 2), name='conv1', kernel_initializer=glorot_uniform(seed=0))
        self.bnoo = BatchNormalization(axis=3, name='bn_conv1')
        self.activ = Activation('relu')
        self.maxpool1 = MaxPooling2D((3, 3), strides=(2, 2))
        
        self.conblock1 = convolutional_block(f=3, filters=[64, 64, 256], stage=2, block='a', s=1)
        self.idblock1 = identity_block( 3, [64, 64, 256], stage=2, block='b')
        self.idblock11 = identity_block( 3, [64, 64, 256], stage=2, block='c')
        
        self.conblock2 = convolutional_block( f=3, filters=[128, 128, 512], stage=3, block='a', s=2)
        self.idblock2 = identity_block(3, [128, 128, 512], stage=3, block='b')
        self.idblock21 = identity_block( 3, [128, 128, 512], stage=3, block='c')
        self.idblock22 = identity_block( 3, [128, 128, 512], stage=3, block='d')
        
        self.conblock3 = convolutional_block( f=3, filters=[256, 256, 1024], stage=4, block='a', s=2)
        self.idblock3 = identity_block( 3, [256, 256, 1024], stage=4, block='b')
        self.idblock31 = identity_block( 3, [256, 256, 1024], stage=4, block='c')
        self.idblock32 = identity_block( 3, [256, 256, 1024], stage=4, block='d')
        self.idblock33 = identity_block( 3, [256, 256, 1024], stage=4, block='e')
        self.idblock34 = identity_block( 3, [256, 256, 1024], stage=4, block='f')
        
        self.conblock4 = convolutional_block( f=3, filters=[512, 512, 2048], stage=5, block='a', s=2)
        self.idblock4 = identity_block( 3, [512, 512, 2048], stage=5, block='b')
        self.idblock41 = identity_block( 3, [512, 512, 2048], stage=5, block='c')
        
        self.avgbool = AveragePooling2D(pool_size=(2, 2), padding='same')
        self.f = Flatten()
        
        self.d1 = Dense(512, activation='relu', name='fc1',kernel_initializer=glorot_uniform(seed=0))
        self.dropout1 = Dropout(.3)
        self.out = Dense( self.num_classes,activation='softmax', name='fc3',kernel_initializer=glorot_uniform(seed=0))
        
    def call(self,inputs):
        x_id = inputs
        x_con = inputs
        
        zero_padding = self.zeropadding(x_id)
        x = self.conn(zero_padding)
        x = self.bnoo(x)
        x = self.activ(x)
        x = self.maxpool1(x)
        
        x = self.conblock1(x)
        x = self.idblock1(x)
        x = self.idblock11(x)
        
        x = self.conblock2(x)
        x = self.idblock2(x)
        x = self.idblock21(x)
        x = self.idblock22(x)
        
        x = self.conblock3(x) 
        x = self.idblock3(x)
        x = self.idblock31(x)
        x = self.idblock32(x)
        x = self.idblock33(x)
        x = self.idblock34(x)
        
        x = self.conblock4(x)
        x = self.idblock4(x)
        x = self.idblock41(x)
        
        x = self.avgbool(x)
        x = self.f(x)
        x = self.d1(x)
        x = self.dropout1(x)
        x = self.out(x)
        
        return x
        