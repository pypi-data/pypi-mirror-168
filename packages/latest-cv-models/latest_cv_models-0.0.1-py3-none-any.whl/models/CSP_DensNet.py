# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 11:51:20 2022

@author: vip
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
import tensorflow.keras.activations as act
from tensorflow.keras.layers import (
    Conv2D,
    Input,
    MaxPool2D,
    Concatenate,
    AveragePooling2D,
    GlobalAveragePooling2D,
    Dropout,
    BatchNormalization,
    Reshape,
    Flatten,
)


def mish(x):
    x = x * (act.tanh(act.softplus(x)))
    return x


class conv_block(tf.keras.layers.Layer):
    def __init__(self , filter , kernel,stride,padding):
        super(conv_block , self).__init__()

        self.conv5 = Conv2D(filters = filter,kernel_size= kernel,strides=stride,padding=padding)

        def call(self,inputs):
            x=inputs
            x=self.conv5(x)
            x = mish(x)
            return x


class nine_block(tf.keras.layers.Layer):
    def __init__(self , filter , ker):
        super(nine_block,self).__init__()
        
        self.conv0 = Conv2D(filter, ker, padding="same")
        
        self.conv1 = Conv2D(filter, 1, padding="same")
        
        self.conv2 = Conv2D(filter, 1, padding="same")
        
    def call(self , inputs):
        x = inputs
        x = self.conv0(x)
        x = mish(x)
        x = self.conv1(x)
        x = mish(x)
        x = self.conv2(x)
        x = mish(x)
        return x   


class dense_block_cspnet(tf.keras.layers.Layer):
    def __init__(self , partition ,filters , times ):
        super(dense_block_cspnet , self ).__init__()
        
        self.conv0 = Conv2D(filters[0], 1, padding="same")
        
        self.conv1 = Conv2D(filters[1], 3, padding="same")
    
        self.conv2 = Conv2D(filters[2], 1, padding="same")
        
        def call(self,inps):
            shape = inps.shape
            features = shape[3] - partition
            part1 = inps
            part1 = inps[:, :, :, 0:features]
            part2 = inps[:, :, :, features:]
            for time in range(0, times):
                part2 = self.conv0(part2)
                part2 = mish(part2)
                part2 = self.conv1(part2)
                part2 = mish(part2)

            part2 = self.conv2(part2)
            part2 = mish(part2)
            inps = Concatenate()([part1, part2])
            return inps
        
        
class CSPDenseNet(tf.keras.Model):
     def __init__(self , num_classes):
        super(CSPDenseNet,self).__init__()
        
        self.num_classes = num_classes
        
        # convblock0
        self.convblock0 = conv_block(filter= 32, kernel= 7, stride= 2, padding='same')
        self.maxpooling0 = MaxPool2D(pool_size=(2, 2), strides=(2, 2))
        
        #DenseBlock0
        self.denseblock0 = dense_block_cspnet( 24, [64, 64, 64], 20)
        self.drop0 = Dropout(0.5)
        self.bn0 = BatchNormalization()
        
        #conblock1
        self.convblock1 = conv_block(filter= 64, kernel= 1, stride= 1, padding='same')
        self.avg1 = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))
        
        # dense block 1
        self.denseblock1 = dense_block_cspnet( 24, [64, 64, 64], 20)
        self.drop1 = Dropout(0.5)
        self.bn1 = BatchNormalization()
        
        #convblock2
        self.convblock2 = conv_block(filter= 64, kernel= 1, stride= 1, padding='same')
        self.avg2 = AveragePooling2D(pool_size=(2, 2), strides=2)

        # dense block 2
        self.desneblock2 = dense_block_cspnet( 24, [64, 64, 64], 20)
        self.drop2 = Dropout(0.5)
        self.bn2 =  BatchNormalization()
        
        #convblock3
        #self.convblock3 = conv_block([{"filter": 64, "kernel": 1, "strides": 1, "padding": "same"}])
        self.convblock3 = conv_block(filter= 64, kernel= 1, stride= 1, padding='same')

        self.avg3 =  AveragePooling2D(pool_size=(2, 2), strides=2)
        
        # nin block
        self.nin = nine_block(self.num_classes, 3)
        self.gavg= GlobalAveragePooling2D()
        self.resh = Reshape((1, 1, self.num_classes))
        self.out = Flatten()
        
        
     def call(self,inputs):
        
        
        x = self.convblock0(inputs)
        x = self.maxpooling0(x)
        x = self.denseblock0 (x)
        x = self.drop0(x)
        x = self.bn0(x) 
        
        x = self.convblock1(x)
        x = self.avg1(x)
        x = self.denseblock1(x)
        x = self.drop1(x)
        x = self.bn1(x) 
        
        x = self.convblock2(x)
        x = self.avg2(x)
        x = self.desneblock2(x)
        x = self.drop2(x)
        x = self.bn2(x) 
        
        x = self.convblock3(x)
        x = self.avg3(x)
        
        x = self.nin(x)
        x = self.gavg(x)
        x = self.resh(x)
        x = self.out(x)
        
        return x        
        
        
