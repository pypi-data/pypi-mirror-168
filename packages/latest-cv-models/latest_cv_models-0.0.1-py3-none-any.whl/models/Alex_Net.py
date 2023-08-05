# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 11:26:31 2022

@author: vip
"""

import keras

from keras import backend as K
from keras.models import Sequential, Model,load_model
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.layers import Dropout, Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D,MaxPool2D
from keras.preprocessing import image
from keras.initializers import glorot_uniform
import tensorflow as tf


class AlexNet(tf.keras.Model):
    def __init__(self , num_classes):
        super(AlexNet,self).__init__()
        
        self.num_classes = num_classes
        
        self.conv1 = Conv2D(filters=96, kernel_size=(11,11), strides=(4,4), activation='relu')
        self.bn1 = BatchNormalization()
        self.maxpool1 = MaxPool2D(pool_size=(3,3))
        
        self.conv2 = Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), activation='relu', padding="same")
        self.bn2 = BatchNormalization()
        self.maxpool2 = MaxPool2D(pool_size=(3,3))
        
        self.conv3 = Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same")
        self.bn3 = BatchNormalization()
        
        self.conv4 = Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same")
        self.bn4 = BatchNormalization()
        
        self.conv5 = Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same")
        self.bn5 = BatchNormalization()
        self.maxpool5 = MaxPool2D(pool_size=(3,3))
        
        self.f1 = Flatten()
        self.dense1 = Dense(4096,activation='relu')
        self.drop1 = Dropout(0.5)
        self.dense2 = Dense(4096,activation='relu')
        self.drop2 = Dropout(0.5)
        self.out = Dense(self.num_classes,activation='softmax')
        
    def call(self,inputs):
        x =  self.conv1(inputs)
        x =  self.bn1(x)
        x = self.maxpool1(x)
        
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.maxpool2(x)
        
        x = self.conv3(x)
        x = self.bn3(x)
        
        x = self.conv4(x)
        x = self.bn4(x)
        
        x = self.conv5(x)
        x = self.bn5(x)
        x = self.maxpool5(x)
        
        x = self.f1(x)
        x = self.dense1(x)
        x = self.drop1(x)
        x = self.dense2(x)
        x = self.drop2(x)
        x = self.out(x)
        
        return x