



from keras import backend as K
from keras.models import Sequential, Model,load_model
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.layers import Dropout,ReLU,Resizing,Layer, Input, add, Dense, concatenate,Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D,GlobalAveragePooling2D
class ConvBlock(Layer):

    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 strides,
                 padding,
                 dilation=1,
                 groups=1,
                 use_bias=False,
                 force_same=False,
                 use_bn=True,
                 bn_eps=1e-5,
                 activation="relu",
                 data_format="channels_last",
                 **kwargs):
        super(ConvBlock, self).__init__(**kwargs)
        assert (in_channels is not None)
        self.activate = (activation is not None)
        self.use_bn = use_bn

        self.conv = Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            dilation=dilation,
            groups=groups,
            use_bias=use_bias,
            force_same=force_same,
            data_format=data_format,
            name="conv")
        if self.use_bn:
            self.bn = BatchNormalization(
                epsilon=bn_eps,
                name="bn")
        if self.activate:
            self.activ = ReLU()

    def call(self, x, training=None):
        x = self.conv(x)
        if self.use_bn:
            x = self.bn(x, training=training)
        if self.activate:
            x = self.activ(x)
        return x


class Conv2d(Layer):
    
    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 strides=1,
                 padding=0,
                 dilation=1,
                 groups=1,
                 use_bias=True,
                 force_same=False,
                 data_format="channels_last",
                 **kwargs):
        super(Conv2d, self).__init__(**kwargs)
        assert (in_channels is not None)
        self.data_format = data_format
        self.use_conv = (groups == 1)
        self.use_dw_conv = (groups > 1) and (groups == out_channels) and (out_channels == in_channels)

        # assert (strides == 1) or (dilation == 1)

        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        if isinstance(strides, int):
            strides = (strides, strides)
        if isinstance(padding, int):
            padding = (padding, padding)
        if isinstance(dilation, int):
            dilation = (dilation, dilation)

        self.use_pad = ((padding[0] > 0) or (padding[1] > 0)) and (not force_same)
        if self.use_pad:
            self.pad = ZeroPadding2D(
                padding=padding,
                data_format=data_format)
       

        assert (not force_same) or ((padding[0] == kernel_size[0] // 2) and (padding[1] == kernel_size[1] // 2) and
                                    (strides[0] == 1) and (strides[0] == strides[1]) and (dilation[0] == 1) and
                                    (dilation[0] == dilation[1]))

        if self.use_conv:
            self.conv = Conv2D(
                filters=out_channels,
                kernel_size=kernel_size,
                strides=strides,
                padding=("valid" if not force_same else "same"),
                data_format=data_format,
                dilation_rate=dilation,
                use_bias=use_bias,
                name="conv")
        elif self.use_dw_conv:
            # assert (dilation[0] == 1) and (dilation[1] == 1)
            self.dw_conv = DepthwiseConv2D(
                kernel_size=kernel_size,
                strides=strides,
                padding=("valid" if not force_same else "same"),
                data_format=data_format,
                dilation_rate=dilation,
                use_bias=use_bias,
                name="dw_conv")
        else:
            assert (groups > 1)
            assert (in_channels % groups == 0)
            assert (out_channels % groups == 0)
            self.groups = groups
            self.convs = []
            for i in range(groups):
                self.convs.append(Conv2D(
                    filters=(out_channels // groups),
                    kernel_size=kernel_size,
                    strides=strides,
                    padding="valid",
                    data_format=data_format,
                    dilation_rate=dilation,
                    use_bias=use_bias,
                    name="convgroup{}".format(i + 1)))

    def call(self, x):
        if self.use_pad:
            x = self.pad(x)
            # x = tf.pad(x, paddings=self.paddings_tf)
        if self.use_conv:
            try:
                x = self.conv(x)
            except tf.errors.InvalidArgumentError as ex:
                if self.conv.dilation_rate != (1, 1):
                    conv_ = Conv2D(
                        filters=self.conv.filters,
                        kernel_size=self.conv.kernel_size,
                        strides=self.conv.strides,
                        padding="valid",
                        data_format=self.data_format,
                        dilation_rate=self.conv.dilation_rate,
                        use_bias=self.conv.use_bias,
                        name="conv_")
                    _ = conv_(x)
                    conv_.weights[0].assign(self.conv.weights[0])
                    if len(self.conv.weights) > 1:
                        conv_.weights[1].assign(self.conv.weights[1])
                    x = conv_(x)
                else:
                    raise ex
            # x = self.conv(x)
        elif self.use_dw_conv:
            x = self.dw_conv(x)
        else:
            yy = []
            xx = tf.split(x, num_or_size_splits=self.groups, axis=get_channel_axis(self.data_format))
            for xi, convi in zip(xx, self.convs):
                yy.append(convi(xi))
            x = tf.concat(yy, axis=get_channel_axis(self.data_format))
        # if self.use_post_pad:
        #     x = self.post_pad(x)
        return x


class MaxPool2d(Layer):

    def __init__(self,
                 pool_size,
                 strides,
                 padding=0,
                 ceil_mode=False,
                 data_format="channels_last",
                 **kwargs):
        super(MaxPool2d, self).__init__(**kwargs)
        if isinstance(pool_size, int):
            pool_size = (pool_size, pool_size)
        if isinstance(strides, int):
            strides = (strides, strides)
        if isinstance(padding, int):
            padding = (padding, padding)

        self.use_stride = (strides[0] > 1) or (strides[1] > 1)
        self.ceil_mode = ceil_mode and self.use_stride
        self.use_pad = (padding[0] > 0) or (padding[1] > 0)

        if self.ceil_mode:
            self.padding = padding
            self.pool_size = pool_size
            self.strides = strides
            self.data_format = data_format
        elif self.use_pad:
            if self.data_format == "channels_first":
                self.paddings_tf = [[0, 0], [0, 0], [padding[0]] * 2, [padding[1]] * 2]
            else:
                self.paddings_tf = [[0, 0], [padding[0]] * 2, [padding[1]] * 2, [0, 0]]

        self.pool = MaxPooling2D(
            pool_size=pool_size,
            strides=strides,
            padding="valid",
            data_format=data_format)

    def call(self, x):
        if self.ceil_mode:
            x_shape = x.get_shape().as_list()
            if self.data_format == "channels_first":
                height = x_shape[2]
                width = x_shape[3]
            else:
                height = x_shape[1]
                width = x_shape[2]
            padding = self.padding
            out_height = float(height + 2 * padding[0] - self.pool_size[0]) / self.strides[0] + 1.0
            out_width = float(width + 2 * padding[1] - self.pool_size[1]) / self.strides[1] + 1.0
            if math.ceil(out_height) > math.floor(out_height):
                padding = (padding[0] + 1, padding[1])
            if math.ceil(out_width) > math.floor(out_width):
                padding = (padding[0], padding[1] + 1)
            if (padding[0] > 0) or (padding[1] > 0):
                if self.data_format == "channels_first":
                    paddings_tf = [[0, 0], [0, 0], [padding[0]] * 2, [padding[1]] * 2]
                else:
                    paddings_tf = [[0, 0], [padding[0]] * 2, [padding[1]] * 2, [0, 0]]
                x = tf.pad(x, paddings=paddings_tf)
        elif self.use_pad:
            x = tf.pad(x, paddings=self.paddings_tf)

        x = self.pool(x)
        return x


class SimpleSequential(Layer):
    
    def __init__(self,
                 **kwargs):
        super(SimpleSequential, self).__init__(**kwargs)
        self.children = []

    def __getitem__(self, i):
        return self.children[i]

    def __len__(self):
        return len(self.children)

    def add(self, layer):
        layer._name = "{}/{}".format(self.name, layer._name)
        self.children.append(layer)

    def call(self, x, training=None):
        for block in self.children:
            x = block(x, training=training)
        return x


class SequentialConcurrent(SimpleSequential):

    def __init__(self,
                 stack=False,
                 cat_input=True,
                 data_format="channels_last",
                 **kwargs):
        super(SequentialConcurrent, self).__init__(**kwargs)
        self.axis = 1 if data_format == "channels_first" else -1
        self.stack = stack
        self.cat_input = cat_input

    def call(self, x, training=None):
        out = [x] if self.cat_input else []
        for block in self.children:
            x = block(x, training=training)
            out.append(x)
        if self.stack:
            out = tf.stack(out, axis=self.axis)
        else:
            out = tf.concat(out, axis=self.axis)
        return out


class VoVUnit(Layer):

    def __init__(self,
                 in_channels,
                 out_channels,
                 branch_channels,
                 num_branches,
                 resize,
                 use_residual,
                 data_format="channels_last",
                 **kwargs):
        super(VoVUnit, self).__init__(**kwargs)
        self.resize = resize
        self.use_residual = use_residual

        if self.resize:
            self.pool = MaxPool2d(
                pool_size=3,
                strides=2,
                ceil_mode=True,
                data_format=data_format,
                name="pool")

        self.branches = SequentialConcurrent(
            data_format=data_format,
            name="branches")
        branch_in_channels = in_channels
        for i in range(num_branches):
            self.branches.add(ConvBlock(
                                in_channels=branch_in_channels,
                                out_channels=branch_channels,
                                kernel_size=3,
                                strides=1,
                                padding=1,
                                data_format=data_format,
                                name="branch{}".format(i + 1)))
            branch_in_channels = branch_channels

        self.concat_conv = ConvBlock(
                                in_channels=(in_channels + num_branches * branch_channels),
                                out_channels=out_channels,
                                kernel_size=1,
                                strides=1,
                                padding=0,
                                groups=1,
                                data_format=data_format,
                                name="concat_conv")
        

    def call(self, x, training=None):
        if self.resize:
            x = self.pool(x)
        if self.use_residual:
            identity = x
        x = self.branches(x, training=training)
        x = self.concat_conv(x, training=training)
        if self.use_residual:
            x = x + identity
        return x



class VoVInitBlock(Layer):

    def __init__(self,
                 in_channels,
                 out_channels,
                 data_format="channels_last",
                 **kwargs):
        super(VoVInitBlock, self).__init__(**kwargs)
        mid_channels = out_channels // 2

        self.conv1 = ConvBlock(in_channels=in_channels,
                                out_channels=mid_channels,
                                kernel_size=3,
                                strides=2,
                                padding=1,
                                data_format=data_format,
                                name="conv1")
        self.conv2 = ConvBlock(in_channels=mid_channels,
                                out_channels=mid_channels,
                                kernel_size=3,
                                strides=1,
                                padding=1,
                                dilation=1,
                                data_format=data_format,
                                name="conv2")
        self.conv3 = ConvBlock(in_channels=mid_channels,
                                out_channels=out_channels,
                                kernel_size=3,
                                strides=2,
                                padding=1,
                                dilation=1,
                                data_format=data_format,
                                name="conv3")

    def call(self, x, training=None):
        x = self.conv1(x, training=training)
        x = self.conv2(x, training=training)
        x = self.conv3(x, training=training)
        return x



class VoVNet(tf.keras.Model):

    def __init__(self,
                 channels,
                 branch_channels,
                 num_branches,
                 in_channels=3,
                 in_size=(224, 224),
                 classes=1000,
                 data_format="channels_last",
                 **kwargs):
        super(VoVNet, self).__init__(**kwargs)
        self.resize = Resizing(height = 224,width = 224)
        self.in_size = in_size
        self.classes = classes
        self.data_format = data_format
        init_block_channels = 128

        self.features = SimpleSequential(name="features")
        self.features.add(VoVInitBlock(
            in_channels=in_channels,
            out_channels=init_block_channels,
            data_format=data_format,
            name="init_block"))
        in_channels = init_block_channels
        for i, channels_per_stage in enumerate(channels):
            stage = SimpleSequential(name="stage{}".format(i + 1))
            for j, out_channels in enumerate(channels_per_stage):
                use_residual = (j != 0)
                resize = (j == 0) and (i != 0)
                stage.add(VoVUnit(
                    in_channels=in_channels,
                    out_channels=out_channels,
                    branch_channels=branch_channels[i][j],
                    num_branches=num_branches,
                    resize=resize,
                    use_residual=use_residual,
                    data_format=data_format,
                    name="unit{}".format(j + 1)))
                in_channels = out_channels
            self.features.add(stage)
        self.features.add(AveragePooling2D(
            pool_size=7,
            strides=1,
            data_format=data_format,
            name="final_pool"))

        self.output1 = Dense(
            units=classes,
            input_dim=in_channels,
            name="output1")
        self.flatten = Flatten(data_format=self.data_format)
    def call(self, x, training=None):
        x = self.resize(x)
        x = self.features(x, training=training)
        x = self.flatten(x)
        x = self.output1(x)
        return x





def get_vovnet(blocks,
               slim=False,
               model_name=None,
               pretrained=False,
               root=os.path.join("~", ".tensorflow", "models"),
               **kwargs):

    if blocks == 27:
        layers = [1, 1, 1, 1]
    elif blocks == 39:
        layers = [1, 1, 2, 2]
    elif blocks == 57:
        layers = [1, 1, 4, 3]
    else:
        raise ValueError("Unsupported VoVNet with number of blocks: {}".format(blocks))

    assert (sum(layers) * 6 + 3 == blocks)

    num_branches = 5
    channels_per_layers = [256, 512, 768, 1024]
    branch_channels_per_layers = [128, 160, 192, 224]
    if slim:
        channels_per_layers = [ci // 2 for ci in channels_per_layers]
        branch_channels_per_layers = [ci // 2 for ci in branch_channels_per_layers]

    channels = [[ci] * li for (ci, li) in zip(channels_per_layers, layers)]
    branch_channels = [[ci] * li for (ci, li) in zip(branch_channels_per_layers, layers)]

    net = VoVNet(
        channels=channels,
        branch_channels=branch_channels,
        num_branches=num_branches,
        **kwargs)



    return net

