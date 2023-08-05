

from keras import backend as K
import tensorflow as tf
tf.config.experimental_run_functions_eagerly(True)


class Conv_block(tf.keras.layers.Layer):
    def __init__(self,growth_rate):
        super(Conv_block, self).__init__()
        self.growth_rate=growth_rate
        self.bn_axis=3
        
        self.bn1=tf.keras.layers.BatchNormalization(axis=self.bn_axis,epsilon=1.001e-5,)
        self.act1=tf.keras.layers.Activation('relu')
        self.conv1=tf.keras.layers.Conv2D(4 * self.growth_rate, 1,use_bias=False,)
        
        self.bn2=tf.keras.layers.BatchNormalization(axis=self.bn_axis,epsilon=1.001e-5,)
        self.act2=tf.keras.layers.Activation('relu')
        self.conv2=tf.keras.layers.Conv2D(self.growth_rate,3,padding='same',use_bias=False,)
        
        self.concatenate=tf.keras.layers.Concatenate(axis=self.bn_axis)
        
    def call(self,inputs):
        x1=inputs
        x=self.bn1(inputs)
        x=self.act1(x)
        x=self.conv1(x)
        x=self.bn2(x)
        x=self.act2(x)
        x=self.conv2(x)
            
        return self.concatenate([x1,x])
        

    

class Dense_block(tf.keras.layers.Layer):
    def __init__(self,blocks):
        super (Dense_block,self).__init__()
        self.blocks=blocks
        self.conv_dict={}
        
        for i in range(self.blocks):
            self.conv_dict["conv{0}".format(i)] = Conv_block(32)
            
        self.keys=list(self.conv_dict.keys())
        
    def call(self,inputs):
        x=inputs
        for i in range(self.blocks):
            x=self.conv_dict[self.keys[i]](x)
        return x
    


class Transition_block(tf.keras.layers.Layer):
    def __init__(self,reduction):
        super (Transition_block,self).__init__()
        self.reduction=reduction
        self.bn_axis=3
        self.bn1=tf.keras.layers.BatchNormalization(axis=self.bn_axis, epsilon=1.001e-5)
        self.act1=tf.keras.layers.Activation('relu')
        #self.conv1=tf.keras.Conv2D(int(tf.keras.backend.int_shape(x)[bn_axis] * reduction), 1,use_bias=False,)
        self.avg=tf.keras.layers.AveragePooling2D(2, strides=2)
        
    def call(self,inputs):
        x=self.bn1(inputs)
        x=self.act1(x)
        x=tf.keras.layers.Conv2D(int(tf.keras.backend.int_shape(x)[self.bn_axis] * self.reduction), 1,use_bias=False,)(x)
        return self.avg(x)



class DenseNet121(tf.keras.models.Model):
    def __init__(self,num_class=1):
        super (DenseNet121,self).__init__()
        self.bn_axis=3
        self.num_class=num_class
        
        self.blocks = [6, 12, 24, 16]

        self.zeropad1=tf.keras.layers.ZeroPadding2D(padding=((3, 3), (3, 3)))
        self.conv1=tf.keras.layers.Conv2D(64, 7, strides=2, use_bias=False,)
        self.bn1=tf.keras.layers.BatchNormalization(axis=self.bn_axis, epsilon=1.001e-5)
        self.act1=tf.keras.layers.Activation('relu')
        self.zeropad2=tf.keras.layers.ZeroPadding2D(padding=((1, 1), (1, 1)))
        self.maxp1=tf.keras.layers.MaxPooling2D(3, strides=2,)
        
        self.dense_block1=Dense_block(self.blocks[0])
        self.transition_block1=Transition_block(.5)
        self.dense_block2=Dense_block(self.blocks[1])
        self.transition_block2=Transition_block(.5)
        self.dense_block3=Dense_block(self.blocks[2])
        self.transition_block3=Transition_block(.5)
        self.dense_block4=Dense_block(self.blocks[3])
        self.transition_block4=Transition_block(.5)
        
        self.bn2=tf.keras.layers.BatchNormalization(axis=self.bn_axis, epsilon=1.001e-5)
        self.act2=tf.keras.layers.Activation('relu')
        self.avg=tf.keras.layers.GlobalAveragePooling2D()
        self.dense=tf.keras.layers.Dense(10,activation='softmax')
        
    def call(self,inputs,training=False):
        x= self.zeropad1(inputs)
        x=self.conv1(x)
        x=self.bn1(x)
        x=self.act1(x)
        x=self.zeropad2(x)
        x=self.maxp1(x)
            
        x=self.dense_block1(x)
        x=self.transition_block1(x)
        x=self.dense_block2(x)
        x=self.transition_block2(x)
        x=self.dense_block3(x)
        x=self.transition_block3(x)
        x=self.dense_block4(x)
        x=self.transition_block4(x)
            
        x=self.bn2(x)
        x=self.act2(x)
        x=self.avg(x)
        x=self.dense(x)
            
        return x

