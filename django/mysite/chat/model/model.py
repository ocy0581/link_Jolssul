
# import tensorflow as tf
# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#   # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
#   try:
#     tf.config.experimental.set_virtual_device_configuration(
#         gpus[0],
#         [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
#     logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#     print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
#   except RuntimeError as e:
#     # Virtual devices must be set before GPUs have been initialized
#     print(e)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import Concatenate
import numpy as np


class BahdanauAttention(keras.layers.Layer):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.units = units
        self.W1 = Dense(units)
        self.W2 = Dense(units)
        self.V = Dense(1)

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'units' : self.units,
            'W1' : self.W1,
            'W2' : self.W2,
            'V' : self.V,
        })
        return config
        
    def call(self, values, query):
        hidden_with_time_axis = tf.expand_dims(query, 1)
        score = self.V(tf.nn.tanh(
            self.W1(values) + self.W2(hidden_with_time_axis)))
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector, attention_weights


class ResidualUnit(keras.layers.Layer):
    def __init__(self, filters, strides=1, activation="relu", **kwargs):
        super().__init__(**kwargs)
        self.filters = filters
        self.activation = keras.activations.get(activation)
        self.main_layers = [
            keras.layers.Conv1D(filters, 3, strides=strides, padding="same", activation = "relu",use_bias=False),
            keras.layers.BatchNormalization(),
            #self.activation,
            keras.layers.Conv1D(filters, 3, strides=1, padding="same", use_bias=False),
            keras.layers.BatchNormalization()]
        self.skip_layers = []
        if strides > 1:
            self.skip_layers = [
                keras.layers.Conv1D(filters, 1, strides=strides,
                                    padding="same", use_bias=False),
                keras.layers.BatchNormalization()]

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'filters' : self.filters,
            'activation' : self.activation,
            'main_layers' : self.main_layers,
            'skip_layers' : self.skip_layers,
        })
        return config

    def call(self, inputs):
        Z = inputs
        for layer in self.main_layers:
            Z = layer(Z)
        skip_Z = inputs
        for layer in self.skip_layers:
            skip_Z = layer(skip_Z)
        return self.activation(Z + skip_Z)
        
class LstmModel(object):
    def __init__(self):
        super().__init__()
        self.answer_set = ['0', '1', '2', '3', '4', '5', '6', '7', '가끔 그렇습니다', '가렵다', '가슴', '감기', '감사합니다', '고열', '골절', '교통사고', '구내염', '귀', '근육통', '눈', '다리', '두드러기', '두통', '등', '따끔거리다', '멍들다', '목', '몸', '몸살', '무릎', '물다', '발목', '부러지다', '붕대', '뼈', '사마귀', '설사', '소화불량', '손', '수술', '심장마비', '쓰러지다', '아픕니다', '안녕하세요', '어깨', '어지럽다', '얼굴', '열', '의사', '임신', '자주 그렇습니다', '찰과상', '코로나', '탈구', '탈모', '토하다', '파상풍', '피', '피부', '허리', '호흡곤란', '화상']
        self.model = self.create_model(self.answer_set)
        self.max_length = 129
        print('init')

    def predictWord(self,data):
        # print(data[0])
        print('input shape', data.shape)
        d = data.reshape((-1, 126))
        d = np.pad(d, ((0, self.max_length - data.shape[0]), (0, 0)), 'constant', constant_values=0)
        d = d.reshape(1, 129, 126)
        print('model input', d.shape)
        self.model.load_weights("/home/link/git/link_Jolssul/django/mysite/chat/model/87-0.0075.hdf5")
        prediction = self.answer_set[np.argmax(self.model.predict(d))]
        print(prediction)
        return prediction

    def create_model(self, answer_set):
        dropout = 0.25
        num_classes = len(answer_set)
        nodesizes = [64, 64, 128]

        inputs = keras.Input(shape=(129, 126))

        lstm = Bidirectional(layers.LSTM(128, return_sequences=True))(inputs)
        lstm = layers.Dropout(rate=dropout)(lstm)  

        for i in range(0,3):    #number of layers random between 1 an 3
            lstm = Bidirectional(layers.LSTM(nodesizes[i],return_sequences=True))(lstm)
            lstm = layers.Dropout(rate=dropout)(lstm)

        #lstm = Bidirectional(layers.LSTM(256))(lstm)
        #lstm = layers.Dr|opout(rate=dropout)(lstm)

        lstm, forward_h, forward_c, backward_h, backward_c = Bidirectional \
        (layers.LSTM(128, return_sequences=True, return_state=True))(lstm)

        state_h = Concatenate()([forward_h, backward_h]) # 은닉 상태
        state_c = Concatenate()([forward_c, backward_c]) # 셀 상태

        attention = BahdanauAttention(128) # 가중치 크기 정의

        context_vector, attention_weights = attention(lstm, state_h)
        dense1 = Dense(128, activation="relu")(context_vector)
        dropout = layers.Dropout(0.)(dense1)

        class_output = layers.Dense(num_classes, activation='softmax', name='class_output')(dense1)

        model = keras.models.Model(inputs=inputs, outputs=[class_output])

        model.compile(loss={
            'class_output': 'categorical_crossentropy', 
            },
            optimizer='Adamax',
            metrics=['accuracy'])
        
        return model