from Parser import Parser
import nltk
from nltk.collocations import *
from gensim.models import word2vec
import jieba
import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.layers import TimeDistributed



batch_size = 1

parser = Parser()
# jieba custom setting.
jieba.set_dictionary('jieba_dict/dict.txt.big')

# load stopwords set
stopwordset = set()
with open('jieba_dict/stopwords.txt','r',encoding='utf-8') as sw:
    for line in sw:
        stopwordset.add(line.strip('\n'))

def transform_y(pos_opinion, neg_opinion):
    y = [0.5]*5
    for category in pos_opinion:
        if category == "服務":
            y[0] = 1.0
        if category == "環境":
            y[1] = 1.0
        if category == "價格":
            y[2] = 1.0
        if category == "交通":
            y[3] = 1.0
        if category == "餐廳":
            y[4] = 1.0

    for category in neg_opinion:
        if category == "服務":
            y[0] = 0.0
        if category == "環境":
            y[1] = 0.0
        if category == "價格":
            y[2] = 0.0
        if category == "交通":
            y[3] = 0.0
        if category == "餐廳":
            y[4] = 0.0
    return y

def segment(line):
    result = []
    words = jieba.cut(line, cut_all=False)
    for word in words:
        if word not in stopwordset:
            result.append(word)
    return result


def review_to_vec(w2v_model):
    x_train = []
    y_train = []
    for line in parser.aspect_review():
        review = segment(line[1])
        pos_opinion = []
        neg_opinion = []
        if len(line[2]) != 0:
            pos_opinion = line[2].split('\t')
        if len(line[3]) != 0:
            neg_opinion = line[3].split('\t')
        y_train.append(transform_y(pos_opinion, neg_opinion))
        sequnence = []
        for character in review:
            try:
                sequnence.append(w2v_model.wv[character])
            except KeyError:
                print ("%s not in vocabulary" %character)
                sequnence.append([0.0] * w2v_model.vector_size)
        x_train.append(sequnence)
    return np.asarray(x_train), np.asarray(y_train)

def build_model(timesteps, vector_size):
    print('Build model...')
    model = Sequential()
    model.add(LSTM(128, dropout=0.3, recurrent_dropout=0.2, return_sequences=False, input_shape=(timesteps, vector_size)))
    model.add(TimeDistributed(Dense(8), input_shape=(timesteps, vector_size)))
    model.add(LSTM(64))
    model.add(Dense(5, activation='sigmoid'))

    # try using different optimizers and different optimizer configs
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


def main():
    w2v_model = word2vec.Word2Vec.load("med250.model.bin")
    x_train, y_train = review_to_vec(w2v_model)
    
    print('Pad sequences (samples x time)')
    x_train = sequence.pad_sequences(x_train)
    print('x_train shape:', x_train.shape)
    print('y_train shape:', y_train.shape)

    lstm_model = build_model(x_train.shape[1], x_train.shape[2])
    print('Train...')
    lstm_model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=15)
    score, acc = lstm_model.evaluate(x_train, y_train,batch_size=batch_size)
    print ("score: %d" %score)
    print ("acc: %d" %acc)

if __name__ == '__main__':
    main()
