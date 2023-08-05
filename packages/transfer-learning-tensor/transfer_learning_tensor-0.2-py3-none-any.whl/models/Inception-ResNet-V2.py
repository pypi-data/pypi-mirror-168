
import keras

from keras import backend as K
from keras.models import Sequential, Model,load_model
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.layers import Activation, AveragePooling2D, BatchNormalization, Concatenate, Conv2D, Dense, GlobalAveragePooling2D, GlobalMaxPooling2D, Input, Lambda, MaxPooling2D, Layer, Flatten, Resizing, Add, Dropout
from keras.preprocessing import image


class StemLayer(tf.keras.layers.Layer):
    def __init__(self,activation = 'relu'):
        super(StemLayer, self).__init__()
        
        self.resize = Resizing(height = 299,width = 299)
        self.conv2d_1 = Conv2D(filters = 32, kernel_size = (3,3), strides =(2,2), padding = 'valid',activation = activation)
        self.conv2d_2 = Conv2D(filters = 32, kernel_size = (3,3), strides = (1,1), padding = 'valid', activation = activation)
        self.conv2d_3 = Conv2D(filters = 64, kernel_size = (3,3), strides = (1,1), padding = 'same', activation = activation) 
        self.max_pool_1 = MaxPooling2D(pool_size=(3,3), strides = (2,2), padding ='valid') 
        self.conv2d_4 = Conv2D(filters = 96, kernel_size = (3,3), strides = (2,2), padding = 'valid', activation = activation)
        self.concat_1 = Concatenate(axis =-1) 
        self.conv2d_5 = Conv2D(filters = 64, kernel_size = (1,1), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_6 = Conv2D(filters = 96, kernel_size = (3,3), strides = (1,1), padding = 'valid', activation = activation) 
        self.conv2d_7 = Conv2D(filters = 64, kernel_size = (1,1), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_8 = Conv2D(filters = 64, kernel_size = (7,1), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_9 = Conv2D(filters = 64, kernel_size = (1,7), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_10 = Conv2D(filters = 96, kernel_size = (3,3), strides = (1,1), padding = 'valid', activation = activation) 
        self.concat_2 = Concatenate(axis =-1)
        self.conv2d_11 = Conv2D(filters = 192, kernel_size = (3,3), strides = (2,2), padding = 'valid', activation = activation) 
        self.max_pool_2 = MaxPooling2D(pool_size=(2,2), strides = (2,2), padding ='valid') 
        self.concat_3 = Concatenate(axis =-1)
        
    def call(self, stem_input ): 
        resize_out = self.resize(stem_input)
        conv1_out = self.conv2d_1(resize_out) 
        conv2_out = self.conv2d_2(conv1_out) 
        conv3_out = self.conv2d_3(conv2_out) 
        maxpool1_out = self.max_pool_1(conv3_out)
        conv4_out = self.conv2d_4(conv3_out) 
        concat1_out = self.concat_1([maxpool1_out,conv4_out])  
        conv5_out = self.conv2d_5(concat1_out)
        conv6_out = self.conv2d_6(conv5_out) 
        conv7_out = self.conv2d_7(concat1_out) 
        conv8_out = self.conv2d_8(conv7_out) 
        conv9_out = self.conv2d_9(conv8_out) 
        conv10_out = self.conv2d_10(conv9_out) 
        concat2_out = self.concat_2([conv6_out, conv10_out])
        conv11_out = self.conv2d_11(concat2_out) 
        maxpool2_out = self.max_pool_2(concat2_out) 
        concat3_out = self.concat_3([conv11_out,maxpool2_out]) 

        return concat3_out 

class InceptionResnetA(tf.keras.layers.Layer):
    def __init__(self, resnet_scale = 0.1, activation = 'relu'):
        self.resnet_scale = resnet_scale
        
        super(InceptionResnetA, self).__init__()
        self.relu_1 = Activation('relu')
        self.conv2d_1 = Conv2D(filters = 32, kernel_size = (1,1), strides =(1,1), padding = 'same', activation = activation) 
        self.conv2d_2 = Conv2D(filters = 32, kernel_size = (1,1), strides =(1,1), padding = 'same', activation = activation)
        self.conv2d_3 = Conv2D(filters = 32, kernel_size = (3,3), strides =(1,1), padding = 'same', activation = activation)
        self.conv2d_4 = Conv2D(filters = 32, kernel_size = (1,1), strides =(1,1), padding = 'same', activation = activation) 
        self.conv2d_5 = Conv2D(filters = 48, kernel_size = (3,3), strides =(1,1), padding = 'same', activation = activation) 
        self.conv2d_6 = Conv2D(filters = 64, kernel_size = (3,3), strides =(1,1), padding = 'same', activation = activation) 

        self.concat_1 = Concatenate(axis=-1)
        self.linear_1 = Dense(384) 
        self.conv2d_7 = Conv2D(filters = 384, kernel_size = (1,1), strides =(1,1), padding = 'same') #
        self.add_layer = Add()
        self.relu_2 = Activation('relu') 
        
    def call(self, stem_out): 
        stem_out = self.relu_1(stem_out) 
        conv1_out = self.conv2d_1(stem_out) 
        conv2_out = self.conv2d_2(stem_out) 
        conv3_out = self.conv2d_3(conv2_out) 
        conv4_out = self.conv2d_4(stem_out) 
        conv5_out = self.conv2d_5(conv4_out) 
        conv6_out = self.conv2d_6(conv5_out) 

        concat1_out = self.concat_1([conv1_out,conv3_out,conv6_out]) 
        concat1_out = self.linear_1(concat1_out)
        conv7_out = self.conv2d_7(concat1_out) 
        out = self.add_layer([stem_out, tf.math.multiply(conv7_out,self.resnet_scale)])  
        final_out = self.relu_2(out) 

        return final_out



class ReductionA(tf.keras.layers.Layer):
    def __init__(self,
                 conv2d_1_num_filter = 384, #n
                 conv2d_2_num_filter = 256, #k
                 conv2d_3_num_filter = 256, #l
                 conv2d_4_num_filter = 384, #m
                 activation = 'relu'):
        super(ReductionA, self).__init__()

        self.max_pool_1 = MaxPooling2D(pool_size=(3,3), strides = (2,2), padding ='valid') #(batch_size,17,17,384)
        self.conv2d_1 = Conv2D(filters = conv2d_1_num_filter, kernel_size = (3,3), strides = (2,2), padding = 'valid', activation = activation) 

        self.conv2d_2 = Conv2D(filters = conv2d_2_num_filter, kernel_size = (1,1), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_3 = Conv2D(filters = conv2d_3_num_filter, kernel_size = (3,3), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_4 = Conv2D(filters = conv2d_4_num_filter, kernel_size = (3,3), strides = (2,2), padding = 'valid', activation = activation) 
        self.concat_1 = Concatenate(axis = -1) 
        
    def call(self, inception_resnetA_out): 
        maxpool1_out = self.max_pool_1(inception_resnetA_out) 
        conv1_out = self.conv2d_1(inception_resnetA_out) 
        conv2_out = self.conv2d_2(inception_resnetA_out)
        conv3_out = self.conv2d_3(conv2_out)
        conv4_out = self.conv2d_4(conv3_out) 
        concat1_out = self.concat_1([maxpool1_out,conv1_out,conv4_out]) 
        return concat1_out 



class InceptionResnetB(tf.keras.layers.Layer):
    def __init__(self, resnet_scale=0.1, activation = 'relu'):
        self.resnet_scale = resnet_scale
        super(InceptionResnetB, self).__init__()
        self.relu_1 = Activation('relu') 
        self.conv2d_1 = Conv2D(filters = 192, kernel_size = (1,1), strides =(1,1), padding = 'same', activation = activation) 
        self.conv2d_2 = Conv2D(filters = 128, kernel_size = (1,1), strides =(1,1), padding = 'same', activation = activation)
        self.conv2d_3 = Conv2D(filters = 160, kernel_size = (1,7), strides =(1,1), padding = 'same', activation = activation) 
        self.conv2d_4 = Conv2D(filters = 192, kernel_size = (7,1), strides =(1,1), padding = 'same', activation = activation)      
        self.concat_1 = Concatenate(axis=-1) 
        self.linear_1 = Dense(1154) 
        self.conv2d_7 = Conv2D(filters = 1152, kernel_size = (1,1), strides =(1,1), padding = 'same') 
        self.add_layer = Add()
        self.relu_2 = Activation('relu') 
        
    def call(self, reductionA_out):  
        reductionA_out = self.relu_1(reductionA_out) 
        conv1_out = self.conv2d_1(reductionA_out) 
        conv2_out = self.conv2d_2(reductionA_out) 
        conv3_out = self.conv2d_3(conv2_out) 
        conv4_out = self.conv2d_4(conv3_out)
        concat_out = self.concat_1([conv1_out, conv4_out]) 
        concat_out = self.linear_1(concat_out) 
        conv7_out = self.conv2d_7 (concat_out) 
        out = self.add_layer([reductionA_out, tf.math.multiply(conv7_out,self.resnet_scale)]) 
        final_out = self.relu_2(out)

        return final_out 





class ReductionB(tf.keras.layers.Layer):
    def __init__(self, activation = 'relu'):
        
        super(ReductionB, self).__init__()
        self.max_pool_1 = MaxPooling2D(pool_size=(3,3), strides = (2,2), padding ='valid') 
        self.conv2d_1 = Conv2D(filters = 256, kernel_size = (1,1), strides = (1,1), padding = 'same', activation = activation) 

        self.conv2d_2 = Conv2D(filters = 384, kernel_size = (3,3), strides = (2,2), padding = 'valid', activation = activation) 
        self.conv2d_3 = Conv2D(filters = 256, kernel_size = (1,1), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_4 = Conv2D(filters = 288, kernel_size = (3,3), strides = (2,2), padding = 'valid', activation = activation) 
        self.conv2d_5 = Conv2D(filters = 256, kernel_size = (1,1), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_6 = Conv2D(filters = 288, kernel_size = (3,3), strides = (1,1), padding = 'same', activation = activation) 
        self.conv2d_7 = Conv2D(filters = 320, kernel_size = (3,3), strides = (2,2), padding = 'valid', activation = activation) 
        self.concat_1 = Concatenate(axis = -1) 
    
    def call(self, input): 
        maxpool1_out = self.max_pool_1(input) 
        conv1_out = self.conv2d_1(input) 
        conv2_out = self.conv2d_2(conv1_out) 
        conv3_out = self.conv2d_3(input) 
        conv4_out = self.conv2d_4(conv3_out) 
        conv5_out = self.conv2d_5(input) 
        conv6_out = self.conv2d_6(conv5_out)
        conv7_out = self.conv2d_7(conv6_out) 

        concat1_out = self.concat_1([maxpool1_out,conv2_out,conv4_out,conv7_out]) 

        return concat1_out 



class InceptionResnetC(tf.keras.layers.Layer):
    def __init__(self, resnet_scale=0.1, activation = 'relu'):
        
        self.resnet_scale = resnet_scale
        super(InceptionResnetC, self).__init__()
        self.relu_1 = Activation('relu') 
        self.conv2d_1 = Conv2D(filters = 192, kernel_size = (1,1), strides =(1,1), padding = 'same', activation = activation)
        self.conv2d_2 = Conv2D(filters = 192, kernel_size = (1,1), strides =(1,1), padding = 'same', activation = activation)
        self.conv2d_3 = Conv2D(filters = 224, kernel_size = (1,3), strides =(1,1), padding = 'same', activation = activation) 
        self.conv2d_4 = Conv2D(filters = 256, kernel_size = (3,1), strides =(1,1), padding = 'same', activation = activation)
        self.concat_1 = Concatenate(axis=-1) 
        self.linear_1 = Dense(2048) 
        self.conv2d_7 = Conv2D(filters = 2144, kernel_size = (1,1), strides =(1,1), padding = 'same') 
        self.add_layer = Add()
        self.relu_2 = Activation('relu')
        
    def call(self, input):  
        reductionB_out = self.relu_1(input) 
        conv1_out = self.conv2d_1(reductionB_out) 
        conv2_out = self.conv2d_2(reductionB_out) 
        conv3_out = self.conv2d_3(conv2_out) 
        conv4_out = self.conv2d_4(conv3_out) 
        concat_out = self.concat_1([conv1_out, conv4_out]) 
        concat_out = self.linear_1(concat_out) 
        conv7_out = self.conv2d_7 (concat_out) 
        out = self.add_layer([reductionB_out, tf.math.multiply(conv7_out,self.resnet_scale)])  
        final_out = self.relu_2(out) 

        return final_out


class InceptionResnetNetwork(tf.keras.Model):
    def __init__(self, num_class,
                 resnetA_scale = 0.1,
                 resnetB_scale = 0.1,
                 resnetC_scale = 0.1
                 ):

        self.num_class = num_class
        super(InceptionResnetNetwork, self).__init__()
        self.stem = StemLayer()
        
        self.inception_resnetA1 = InceptionResnetA(resnetA_scale)
        self.inception_resnetA2 = InceptionResnetA(resnetA_scale)
        self.inception_resnetA3 = InceptionResnetA(resnetA_scale)
        self.inception_resnetA4 = InceptionResnetA(resnetA_scale)
        self.inception_resnetA5 = InceptionResnetA(resnetA_scale)

        self.reductionA = ReductionA()

        self.inception_resnetB1 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB2 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB3 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB4 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB5 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB6 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB7 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB8 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB9 = InceptionResnetB(resnetB_scale)
        self.inception_resnetB10 = InceptionResnetB(resnetB_scale)

        self.reductionB = ReductionB()

        self.inception_resnetC1 = InceptionResnetC(resnetC_scale)
        self.inception_resnetC2 = InceptionResnetC(resnetC_scale)
        self.inception_resnetC3 = InceptionResnetC(resnetC_scale)
        self.inception_resnetC4 = InceptionResnetC(resnetC_scale)
        self.inception_resnetC5 = InceptionResnetC(resnetC_scale)

        self.average_pool = GlobalAveragePooling2D()
        self.dropout = Dropout(rate = 0.2)
        self.classifier = Dense(self.num_class,
                                activation = 'softmax')

    def call(self,input):
        stem_out = self.stem(input)
        inception_resnetA1_out = self.inception_resnetA1(stem_out)
        inception_resnetA2_out = self.inception_resnetA2(inception_resnetA1_out)
        inception_resnetA3_out = self.inception_resnetA3(inception_resnetA2_out)
        inception_resnetA4_out = self.inception_resnetA4(inception_resnetA3_out)
        inception_resnetA5_out = self.inception_resnetA5(inception_resnetA4_out)

        reductionA_out = self.reductionA(inception_resnetA5_out)

        inception_resnetB1_out = self.inception_resnetB1(reductionA_out)
        inception_resnetB2_out = self.inception_resnetB2(inception_resnetB1_out)
        inception_resnetB3_out = self.inception_resnetB3(inception_resnetB2_out)
        inception_resnetB4_out = self.inception_resnetB4(inception_resnetB3_out)
        inception_resnetB5_out = self.inception_resnetB5(inception_resnetB4_out)
        inception_resnetB6_out = self.inception_resnetB6(inception_resnetB5_out)
        inception_resnetB7_out = self.inception_resnetB7(inception_resnetB6_out)
        inception_resnetB8_out = self.inception_resnetB8(inception_resnetB7_out)
        inception_resnetB9_out = self.inception_resnetB9(inception_resnetB8_out)
        inception_resnetB10_out = self.inception_resnetB10(inception_resnetB9_out)

        reductionB_out = self.reductionB(inception_resnetB10_out)

        inception_resnetC1_out = self.inception_resnetC1(reductionB_out)
        inception_resnetC2_out = self.inception_resnetC2(inception_resnetC1_out)
        inception_resnetC3_out = self.inception_resnetC3(inception_resnetC2_out)
        inception_resnetC4_out = self.inception_resnetC4(inception_resnetC3_out)
        inception_resnetC5_out = self.inception_resnetC5(inception_resnetC4_out)

        average_pool_out = self.average_pool(inception_resnetC5_out)
        drop_out = self.dropout(average_pool_out)
        prob_out = self.classifier(drop_out)

        return prob_out 

