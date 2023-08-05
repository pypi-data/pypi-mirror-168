


import tensorflow  as tf
class VGG19(Model):
     def __init__(self,num_classes=1):
        super(VGG19, self).__init__()
        
        self.num_classes=num_classes
        self.conv11=tf.keras.layers.Conv2D(64, (3, 3),activation='relu',padding='same')
        self.conv12=tf.keras.layers.Conv2D(64, (3, 3),activation='relu',padding='same')
        self.max1=tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2))
        
        self.conv21=tf.keras.layers.Conv2D(128, (3, 3),activation='relu',padding='same')
        self.conv22=tf.keras.layers.Conv2D(128, (3, 3),activation='relu',padding='same')
        self.max2=tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2))
        
        self.conv31=tf.keras.layers.Conv2D(256, (3, 3),activation='relu',padding='same')
        self.conv32=tf.keras.layers.Conv2D(256, (3, 3),activation='relu',padding='same')
        self.conv33=tf.keras.layers.Conv2D(256, (3, 3),activation='relu',padding='same')
        self.conv34=tf.keras.layers.Conv2D(256, (3, 3),activation='relu',padding='same')
        self.max3=tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2))
        
        self.conv41=tf.keras.layers.Conv2D(512, (3, 3),activation='relu',padding='same')
        self.conv42=tf.keras.layers.Conv2D(512, (3, 3),activation='relu',padding='same')
        self.conv43=tf.keras.layers.Conv2D(512, (3, 3),activation='relu',padding='same')
        self.conv44=tf.keras.layers.Conv2D(512, (3, 3),activation='relu',padding='same')
        self.max4=tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2))
        
        self.conv51=tf.keras.layers.Conv2D(512, (3, 3),activation='relu',padding='same')
        self.conv52=tf.keras.layers.Conv2D(512, (3, 3),activation='relu',padding='same')
        self.conv53=tf.keras.layers.Conv2D(512, (3, 3),activation='relu',padding='same')
        self.conv54=tf.keras.layers.Conv2D(512, (3, 3),activation='relu',padding='same')
        self.max5=tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2))
        self.gap =tf.keras.layers.GlobalAveragePooling2D()
        self.dense=tf.keras.layers.Dense(self.num_classes,activation='softmax')
      
     def call(self,inputs, training=False):
            x=self.conv11(inputs)
            x=self.conv12(x)
            x=self.max1(x)
            
            x=self.conv21(x)
            x=self.conv22(x)
            x=self.max2(x)
            
            x=self.conv31(x)
            x=self.conv32(x)
            x=self.conv33(x)
            x=self.conv34(x)
            x=self.max3(x)
            
            x=self.conv41(x)
            x=self.conv42(x)
            x=self.conv43(x)
            x=self.conv44(x)
            x=self.max4(x)
            
            x=self.conv51(x)
            x=self.conv52(x)
            x=self.conv53(x)
            x=self.conv54(x)
            x=self.max5(x)
            x=self.gap(x)
            x=self.dense(x)
            return x

