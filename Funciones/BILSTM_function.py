import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

import Funciones.text_results_function as text_results

from tensorflow.python.util import deprecation
from keras import backend
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import TimeDistributed
from keras.layers import Bidirectional
from keras.layers import Dropout

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

def rmse(y_true, y_pred):
    return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))

def model_BILSTM(data,parametros,name_param,periodos,graph_bool,aleatoridad,DataValidation):
    resultado = None
    resultado_prom=[]
    resultado_val=[]
    dic_resProm={}
    dic_resVal = {}
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    optimizer = parametros['optimizer']
    learning_rate = parametros['learning_rate']
    units_memory = parametros['units_memory']
    dense=parametros['dense']
    epoch = parametros['epoch']
    momentum=parametros['momentum']

    if optimizer == 'adam':
        opt=tf.keras.optimizers.Adam(learning_rate=learning_rate)
    elif optimizer=='SGD':
        if momentum:
            opt = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=momentum)
        else:
            opt = tf.keras.optimizers.SGD(learning_rate=learning_rate)

    #Variables Evaluacion Promedio
    acu_prom=0.0
    pre_prom=0.0
    rec_prom=0.0
    f1_prom=0.0
    kap_prom = 0.0
    auc_prom = 0.0
    cm_prom=None
    cm_exist=False
    acu_list=[]

    X=data[2]
    y=data[3]

    Xval=data[4]
    yval=data[5]

    total_iteracion=periodos

    # Variables Evaluacion TOP 1
    acu_best=0.0
    pre_best=0.0
    rec_best=0.0
    f1_best=0.0
    kap_best=0.0
    auc_best=0.0

    for iteracion in range(total_iteracion):

        if aleatoridad and DataValidation:
            Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.30, random_state=None, shuffle=True)
        elif DataValidation:
            Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.30, random_state=42, shuffle=True)
        else:
            Xtrain=data[2]
            ytrain=data[3]
            Xtest=data[4]
            ytest=data[5]

        max_length = Xtrain.shape[1]

        Xtrain_LSTM=Xtrain.reshape(Xtrain.shape[1], Xtrain.shape[0], 1)
        Xtest_LSTM = Xtest.reshape(Xtest.shape[1], Xtest.shape[0], 1)
        ytrain_LSTM = np.zeros(shape=(Xtrain.shape[1],ytrain.shape[0],1), dtype=int)
        ytest_LSTM = np.zeros(shape=(Xtest.shape[1],ytest.shape[0],1), dtype=int)
        for i in range(ytrain_LSTM.shape[0]):
            ytrain_LSTM[i, 0:, 0] = ytrain[0:]
        for i in range(ytest_LSTM.shape[0]):
            ytest_LSTM[i, 0:, 0] = ytest[0:]

        # define LSTM
        model = Sequential()
        #model.add(Bidirectional(LSTM(units_memory, return_sequences=True), input_shape=(max_length, 1))) #valores de salida concatenados
        model.add(Bidirectional(LSTM(units_memory, return_sequences=True), input_shape=(max_length, 1)))       #Caracteristicas = Total de pacientes
        #model.add(Dropout(dropout))
        model.add(TimeDistributed(Dense(dense, activation='sigmoid')))
        print(model.summary())
        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy',rmse])   #problema de clasificación binaria

        history=model.fit(Xtrain_LSTM, ytrain_LSTM, validation_data=(Xtest_LSTM, ytest_LSTM), epochs=epoch, batch_size=1, verbose=2)

        # evaluate the model
        scores_train = model.evaluate(Xtrain_LSTM, ytrain_LSTM,batch_size=1, verbose=2)
        print("Accuracy Train: %.2f%%" % (scores_train[1] * 100))

        #Model Evaluate
        # predict probabilities for test set
        yhat_probs = model.predict(Xtest_LSTM, verbose=0)
        # predict crisp classes for test set
        yhat_classes = (model.predict(Xtest_LSTM) > 0.5).astype("int32")
        ytest=ytest_LSTM[0,:,0]
        y_probs = yhat_probs[0,:,0]
        y_classes = yhat_classes[0,:,0]

        # accuracy: (tp + tn) / (p + n)
        accuracy = accuracy_score(ytest, y_classes)
        # precision tp / (tp + fp)
        precision = precision_score(ytest, y_classes)
        # recall: tp / (tp + fn)
        recall = recall_score(ytest, y_classes)
        # f1: 2 tp / (2 tp + fp + fn)
        f1 = f1_score(ytest, y_classes)
        # kappa
        kappa = cohen_kappa_score(ytest, y_classes)
        # ROC AUC
        auc = roc_auc_score(ytest, y_probs)
        # confusion matrix
        matrix = confusion_matrix(ytest, y_classes)

        acu_list.append(accuracy)
        acu_prom = acu_prom + accuracy
        pre_prom = pre_prom + precision
        rec_prom = rec_prom + recall
        f1_prom = f1_prom + f1
        kap_prom = kap_prom + kappa
        auc_prom = auc_prom + auc
        if cm_prom is None:
            cm_prom = matrix
        if cm_exist is True:
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    cm_prom[j][k] = cm_prom[j][k] + matrix[j][k]
        cm_exist = True

        #GUARDAR LOS MEJORES RESULTADOS EXISTENTES CON RESPECTO AL VALOR F1
        if f1>f1_best:
            f1_best=f1
            acu_best=accuracy
            pre_best=precision
            rec_best=recall
            kap_best=kappa
            auc_best=auc

        name_best='Best_' + str(name_param) +'_F1-'+str(round(f1_best,2))+'_iter-'+str(iteracion)+'_txt-'

        print('\tIteracion: ',iteracion)
        print('\tAccuracy: %f' % accuracy)
        print('\tPrecision: %f' % precision)
        print('\tRecall: %f' % recall)
        print('\tF1 score: %f' % f1)
        print('\tCohens kappa: %f' % kappa)
        print('\tROC AUC: %f' % auc)
        print('\tMatriz de Confusion:')
        print(matrix)
        print('\n')
        # FIN DE ITERACIONES ********************************************************************************
    result_best = [('Accuracy',acu_best), ('Precision',pre_best), ('Recall',rec_best), ('F1',f1_best), ('Kappa',kap_best), ('AUC',auc_best)]

    #GUARDAR MEJORES RESULTADOS INDIVIDUALES EN TEXTO CON NOMBRE NO REPETITIVO Y CONSECUTIVO CON RESPECTO A EXISTENTES
    text_results.save_best_result(result_best,name_best)

    # RESULTADOS NN DE LAS ITERACIONES
    acu_prom = round(acu_prom / total_iteracion, 3)
    pre_prom = round(pre_prom / total_iteracion, 3)
    rec_prom = round(rec_prom / total_iteracion, 3)
    f1_prom = round(f1_prom / total_iteracion, 3)
    kap_prom = round(kap_prom / total_iteracion, 3)
    auc_prom = round(auc_prom / total_iteracion, 3)

    for j in range(len(cm_prom)):
        for k in range(len(cm_prom[j])):
            if cm_prom[j][k] > 0:
                cm_prom[j][k] = round(cm_prom[j][k] / total_iteracion)

    name_prom = 'Prom_'+ str(name_param) + '_F1-' + str(round(f1_prom, 2)) + '_txt-'
    result_prom=[('Accuracy_prom',acu_prom),('Precision_prom',pre_prom),('Recall_prom',rec_prom),('F1_prom',f1_prom),('Kappa_prom',kap_prom),('AUC_prom',auc_prom),('CM_prom',cm_prom)]
    text_results.save_best_result(result_prom, name_prom)

    print('\nResultados Finales Promediados'.upper())
    print('Accuracy: %f' % acu_prom)
    print('Precision: %f' % pre_prom)
    print('Recall: %f' % rec_prom)
    print('F1 score: %f' % f1_prom)
    print('Cohens kappa: %f' % kap_prom)
    print('ROC AUC: %f' % auc_prom)
    print('Matriz de Confusion:')
    print(cm_prom)
    print('\n')

    # Mejores iteraciones
    res1 = 0
    res2 = 100
    acu_index = None
    for i in acu_list:
        if i < 1:
            res1 = abs(acu_prom - i)
            if res1 == 0:
                acu_index = acu_list.index(i)
                break
            elif res1 < res2:
                res2 = res1
                acu_index = acu_list.index(i)

    if not acu_index == None:
        print('Mejor iteracion: ' + str(acu_index + 1) + ' con exactitud de: '
              + str(round(acu_list[acu_index], 3)) + ' con respeto al promedio de: '
              + str(round(acu_prom, 3)))
    else:
        print('NO HAY ITERACION CON EXACTITUD CONFIABLE')

    if graph_bool:
            # plot metrics
        fig, axs = plt.subplots(3)
            # plot loss during training
        axs[0].set_title('Loss')
        axs[0].plot(history.history['loss'], label='train')
        axs[0].plot(history.history['val_loss'], label='test')
        axs[0].set(xlabel='Epochs', ylabel='Loss')
        axs[0].legend()
            # plot accuracy during training
        axs[1].set_title('Accuracy')
        axs[1].plot(history.history['accuracy'], label='train')
        axs[1].plot(history.history['val_accuracy'], label='test')
        axs[1].set(xlabel='Epochs', ylabel='Accuracy')
        axs[1].legend()
            # plot RMSE during training
        axs[2].set_title('Root Mean Square Error')
        axs[2].plot(history.history['rmse'],'tab:blue',label='train')
        axs[2].plot(history.history['val_rmse'],'tab:orange', label='test')
        axs[2].set(xlabel='Epochs', ylabel='RMSE')
        axs[2].legend()

        for ax in fig.get_axes():
            ax.label_outer()
        #plt.show()
        name_graph= str(os.path.abspath(os.getcwd())) + '\\Graficas\\Graph_'+str(name_param)+'.png'
        plt.savefig(name_graph)

    resultado_prom=[acu_prom,pre_prom,rec_prom,f1_prom,kap_prom,auc_prom,cm_prom]
    dic_resProm = {
        'Accuracy_prom': acu_prom,
        'Precision_prom': pre_prom,
        'Recall_prom': rec_prom,
        'F1_prom': f1_prom,
        'Kappa_prom': kap_prom,
        'AUC_prom': auc_prom,
        'CM_prom': cm_prom
    }

    if DataValidation:
        #PRUEBA DE PARAMETROS..............................................................................................
        Xval_LSTM = Xval.reshape(Xval.shape[1], Xval.shape[0], 1)
        yval_LSTM = np.zeros(shape=(Xval.shape[1], yval.shape[0], 1), dtype=int)
        for i in range(yval_LSTM.shape[0]):
            yval_LSTM[i, 0:, 0] = yval[0:]

        yhat_val = model.predict(Xval_LSTM, verbose=0)
        yhat_val_classes = (model.predict(Xval_LSTM) > 0.5).astype("int32")
        yval_test = yval_LSTM[0, :, 0]
        yval_probs = yhat_val[0, :, 0]
        yval_classes = yhat_val_classes[0, :, 0]

        acu_val = accuracy_score(yval_test, yval_classes)
        pre_val = precision_score(yval_test, yval_classes)
        rec_val = recall_score(yval_test, yval_classes)
        f1_val = f1_score(yval_test, yval_classes)
        kap_val = cohen_kappa_score(yval_test, yval_classes)
        auc_val = roc_auc_score(yval_test, yval_probs)
        cm_val = confusion_matrix(yval_test, yval_classes)

        resultado_val = [acu_val, pre_val, rec_val, f1_val, kap_val, auc_val, cm_val]
        dic_resVal = {
            'Accuracy_prom': acu_val,
            'Precision_prom': pre_val,
            'Recall_prom': rec_val,
            'F1_prom': f1_val,
            'Kappa_prom': kap_val,
            'AUC_prom': auc_val,
            'CM_prom': cm_val
        }

        name_val = 'Val_'+ str(name_param) + '_F1-' + str(round(f1_val, 2)) + '_txt-'
        result_val=[('Accuracy_val',acu_val),('Precision_val',pre_val),('Recall_val',rec_val),('F1_val',f1_val),('Kappa_val',kap_val),('AUC_val',auc_val),('CM_val',cm_val)]
        text_results.save_val_result(result_val, name_val)

        print('\nResultados con datos de validacion**************************************************************'.upper())
        print('Accuracy: %f' % acu_val)
        print('Precision: %f' % pre_val)
        print('Recall: %f' % rec_val)
        print('F1 score: %f' % f1_val)
        print('Cohens kappa: %f' % kap_val)
        print('ROC AUC: %f' % auc_val)
        print('Matriz de Confusion:')
        print(cm_val)
        print('\n')
        print('FIN DE MODELADO ___________________________________________________________________________________________')


    resultado=[resultado_prom,resultado_val]
    return resultado
