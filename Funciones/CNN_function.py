import os
import fasttext

from numpy import asarray
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.models import Sequential

def load_embedding(filename):
    ruta_case_cbow = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\ModelVec\\"+str(filename)
    file = open(ruta_case_cbow, encoding="utf8")
    lines = file.readlines()
    file.close()

    embedding = dict()

    for line in lines:
        parts = line.split()
        embedding[parts[0]] = asarray(parts[1:], dtype='float32')
    return embedding

def model_CNN(data,resumen):
    resultado=None
    WE_vector_input=data[0]
    Xtrain=data[2]
    Xtest = data[3]
    ytrain=data[4]
    ytest=data[5]

    embedding_vectors=resumen['CBOW_embedding_layer_final']
    vocab_size=embedding_vectors.shape[0]
    vector_size=embedding_vectors.shape[1]
    max_length=Xtrain.shape[1]

    embedding_layer = Embedding(vocab_size, vector_size, weights=[embedding_vectors], input_length=max_length, trainable=False)

    # Definir Modelo    sigmoid | tanh  | relu
    model = Sequential()
    model.add(embedding_layer)
    model.add(Conv1D(filters=258, kernel_size=5, activation='sigmoid'))
    model.add(MaxPooling1D(pool_size=3))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    print(model.summary())
    # compile network
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])       #problema de clasificación binaria
    # fit network
    model.fit(Xtrain, ytrain, epochs=100, verbose=2)
    # evaluate
    loss, acc = model.evaluate(Xtest, ytest, verbose=0)
    print('Test Accuracy: %f' % (acc * 100))

    return resultado
