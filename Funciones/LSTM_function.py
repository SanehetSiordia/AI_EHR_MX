# LSTM for sequence classification in the IMDB dataset
import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.layers import Dropout
from keras.preprocessing import sequence

def model_LSTM(data):
    resultado=None

    interrogatorios = data[-1]
    WE_vector_input = data[0]
    Xtrain = data[2]
    Xtest = data[3]
    ytrain = data[4]
    ytest = data[5]

    max_text_length = max([len(s.split()) for s in interrogatorios])     #Maximo de palabras encontradas en todos los interrogatorios.
    max_vector_length=Xtrain.shape[1]   #Longitud del vector de palabras maximo (300 por ser la representacion de una oracion)
    embedding_vector_length=Xtrain.shape[1] #capa incrustada que utiliza vectores de longitud de 300 para representar cada oracion.

    # create the model
    model = Sequential()
    model.add(Embedding(max_text_length, embedding_vector_length, input_length=max_vector_length))
    #model.add(Dropout(0.2))     #técnica para combatir el sobreajuste en sus modelos LSTM
    model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    #model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))       #Activacion sigmoide por que se busca clasificacion binaria (0 y 1)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(Xtrain, ytrain, epochs=10, batch_size=64)

    # Final evaluation of the model
    scores = model.evaluate(Xtest, ytest, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1] * 100))
    return resultado