# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 12:09:02 2022

@author: vip
"""

import tensorflow as tf
from keras import backend as K
from keras.models import Sequential, Model,load_model
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.layers import Dropout,ReLU,Layer, Input, add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D,MaxPool2D
from keras.preprocessing import image
from keras.initializers import glorot_uniform


class SKNet(Model):

    def __init__(self, num_classes):
        super(SKNet, self).__init__()

        self.num_classes = num_classes

        ## B1
        self.conv1_a = Conv2D(filters=16, kernel_size=3, strides=1, padding="SAME")
        self.bn1_a = BatchNormalization()
        self.conv1_b = Conv2D(filters=16, kernel_size=5, strides=1, padding="SAME")
        self.bn1_b = BatchNormalization()

        self.fc1 = Dense(8, activation=None)
        self.bn1_fc = BatchNormalization()

        self.fc1_a = Dense(16, activation=None)


        ## B2
        self.conv2_a = Conv2D(filters=32, kernel_size=3, strides=1, padding="SAME")
        self.bn2_a = BatchNormalization()
        self.conv2_b = Conv2D(filters=32, kernel_size=5, strides=1, padding="SAME")
        self.bn2_b = BatchNormalization()

        self.fc2 = Dense(16, activation=None)
        self.bn2_fc = BatchNormalization()

        self.fc2_a = Dense(32, activation=None)


        ## B3
        self.conv3_a = Conv2D(filters=64, kernel_size=3, strides=1, padding="SAME")
        self.bn3_a = BatchNormalization()
        self.conv3_b = Conv2D(filters=64, kernel_size=5, strides=1, padding="SAME")
        self.bn3_b = BatchNormalization()

        self.fc3 = Dense(32, activation=None)
        self.bn3_fc = BatchNormalization()

        self.fc3_a = Dense(64, activation=None)


        ## OUTPUT LAYER
        self.fc_out = Dense(self.num_classes, activation=None)

        self.maxpool = MaxPool2D(pool_size=(2, 2))

    def call(self, inputs):


        # Split-1
        u1_a = tf.keras.activations.relu(self.bn1_a(self.conv1_a(inputs)))
        u1_b = tf.keras.activations.relu(self.bn1_b(self.conv1_b(inputs)))

        # Fuse-1
        u1 = u1_a + u1_b
        s1 = tf.math.reduce_sum(u1, axis=(1, 2))
        z1 = tf.keras.activations.relu(self.bn1_fc(self.fc1(s1)))

        # Select-1
        a1 = tf.keras.activations.softmax(self.fc1_a(z1))
        a1 = tf.expand_dims(a1, 1)
        a1 = tf.expand_dims(a1, 1)
        b1 = 1 - a1
        v1 = (u1_a * a1) + (u1_b * b1)
        
        p1 = self.maxpool(v1)
        
        #################

        # Split-2
        u2_a = tf.keras.activations.relu(self.bn2_a(self.conv2_a(p1)))
        u2_b = tf.keras.activations.relu(self.bn2_b(self.conv2_b(p1)))

        # Fuse-2
        u2 = u2_a + u2_b
        s2 = tf.math.reduce_sum(u2, axis=(1, 2))
        z2 = tf.keras.activations.relu(self.bn2_fc(self.fc2(s2)))

        # Select-2
        a2 = tf.keras.activations.softmax(self.fc2_a(z2))
        a2 = tf.expand_dims(a2, 1)
        a2 = tf.expand_dims(a2, 1)
        b2 = 1 - a2
        v2 = (u2_a * a2) + (u2_b * b2)
        
        p2 = self.maxpool(v2)

        #######################
        
        # Split-3
        u3_a = tf.keras.activations.relu(self.bn3_a(self.conv3_a(p2)))
        u3_b = tf.keras.activations.relu(self.bn3_b(self.conv3_b(p2)))

        # Fuse-3
        u3 = u3_a + u3_b
        s3 = tf.math.reduce_sum(u3, axis=(1, 2))
        z3 = tf.keras.activations.relu(self.bn3_fc(self.fc3(s3)))

        # Select-3
        a3 = tf.keras.activations.softmax(self.fc3_a(z3))
        a3 = tf.expand_dims(a3, 1)
        a3 = tf.expand_dims(a3, 1)
        b3 = 1 - a3
        v3 = (u3_a * a3) + (u3_b * b3)
        

        gap = tf.math.reduce_sum(v3, axis=(1, 2))
        
        out = self.fc_out(gap)
        

        return out