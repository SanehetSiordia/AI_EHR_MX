import os
import string
import fasttext
import numpy as np
import pandas as pd
import itertools

from keras.preprocessing.text import Tokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.snowball import SnowballStemmer

#PREPROCESAMIENTO DE TEXTO  ********************************************************************************************

def clean_text_setence(text):
    resultado=None

    # save setences raw ---------------------------------------------------------------------------
    f = open(str(os.path.abspath(os.getcwd())) +'\\TextFiles\\parrafo_raw.txt', 'w+')
    f.write(str(text))
    f.close()
    #------------------------------------------------------------------------------------------

    # separacion del texto en tokens
    tokens = word_tokenize(text)
    # convierte tokens en minuscula
    tokens = [w.lower() for w in tokens]
    # remueve signos de puntuacion
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remueve tokens remantentes que no son alfabeticos (especios en blanco, numeros, etc...)
    words = [word for word in stripped if word.isalpha()]
    # fitro para quitar "stop words" o palabras de no contenido (set de 313 palabras en total)
    stop_words = set(stopwords.words('spanish'))
    words = [w for w in words if not w in stop_words]

    #convercion de tokens en sentence
    parrafo=str(words[0])
    for w in words[1:]: parrafo=str(parrafo)+' '+str(w)

    # save setences clean ---------------------------------------------------------------------------
    f = open(str(os.path.abspath(os.getcwd())) +'\\TextFiles\\parrafo_limpio.txt', 'w+')
    f.write(str(parrafo))
    f.close()
    #------------------------------------------------------------------------------------------

    resultado=parrafo
    return resultado

def clean_tokens(text):
    resultado=None

    # Clean Text Tokens---------------------------------------------------------------------
    # separacion del texto en tokens
    tokens = word_tokenize(text)
    # convierte tokens en minuscula
    tokens = [w.lower() for w in tokens]
    # remueve signos de puntuacion
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remueve tokens remantentes que no son alfabeticos (especios en blanco, numeros, etc...)
    words = [word for word in stripped if word.isalpha()]
    # fitro para quitar "stop words" o palabras de no contenido (set de 313 palabras en total)
    stop_words = set(stopwords.words('spanish'))
    words = [w for w in words if not w in stop_words]
    # Obtencion de la raiz de la palabra (algoritmo Porter para ingles/ Porter2 o snowball para español)
    Snowball_stemmer = SnowballStemmer('spanish')
    stemmed = [Snowball_stemmer.stem(word) for word in words]

    vocab = Counter()
    vocab.update(words)

    # save tokens clean ---------------------------------------------------------------------------
    f = open(str(os.path.abspath(os.getcwd())) +'\\TextFiles\\tokens_limpio.txt', 'w+')
    f.write(str(words))
    f.close()
    #------------------------------------------------------------------------------------------

    resultado = [words,vocab]
    return resultado


#VECTORIZADO    ********************************************************************************************************

def sentences_embedding(dict_notas_sin_vector):
    resultado=None
    dict_notas_con_vector={}
    dict_iterador = {}
    parrafo_inicial = ''
    parrafo_final = ''
    parrafo_clean_inicial=''
    parrafo_clean_final=''

    #Cargar Modelos para Vectorizar
    print('\n\tcargando modelos fasttext para vectorizar parrafo'.upper())
    ruta_case_cbow = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\bio_cased_cbow.bin"
    ruta_case_skipgram = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\bio_cased_skipgram.bin"
    model_case_cbow = fasttext.load_model(ruta_case_cbow)
    model_case_skipgram = fasttext.load_model(ruta_case_skipgram)

        #Loop para vectorizar y guardar en diccionario
    for key in dict_notas_sin_vector.keys():
        dict_iterador.clear()

        dict_iterador=dict_notas_sin_vector[key].copy()
        parrafo_inicial = str(dict_iterador['interrogatorio_inicial'])
        parrafo_final = str(dict_iterador['interrogatorio_final'])

        parrafo_clean_inicial=clean_text_setence(parrafo_inicial)
        parrafo_clean_final=clean_text_setence(parrafo_final)

        vector_setence_inicial_cbow = model_case_cbow.get_sentence_vector(parrafo_clean_inicial)
        vector_setence_inicia_skipgram = model_case_skipgram.get_sentence_vector(parrafo_clean_inicial)

        vector_setence_final_cbow = model_case_cbow.get_sentence_vector(parrafo_clean_final)
        vector_setence_final_skipgram = model_case_skipgram.get_sentence_vector(parrafo_clean_final)

        dict_iterador['vectorFastText_CBOW_int_inicial']=vector_setence_inicial_cbow
        dict_iterador['vectorFastText_SKIMGRAM_int_inicial']=vector_setence_inicia_skipgram

        dict_iterador['vectorFastText_CBOW_int_final']=vector_setence_final_cbow
        dict_iterador['vectorFastText_SKIMGRAM_int_final']=vector_setence_final_skipgram
        dict_notas_con_vector[key]=dict_iterador.copy()

    print('\n\tGuardando valores de word embedding en diccionario...'.upper())
    resultado=dict_notas_con_vector
    return resultado


def word_embedding_fasttext(dict_notas_sin_vector):
    resultado=[]

    dict_WE_vector={}
    dict_Resumen={}
    dict_iterador = {}

    #Cargar Modelos para Vectorizar
    print('\n\tcargando modelos fasttext para vectorizar palabras'.upper())
    ruta_bio_cbow_cased = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\bio_cased_cbow.bin"
    #ruta_bio_skipgram_cased = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\bio_cased_skipgram.bin"
    model_bio_cbow_cased = fasttext.load_model(ruta_bio_cbow_cased)
    #model_bio_skipgram_cased = fasttext.load_model(ruta_bio_skipgram_cased)

    #ruta_bio_cbow_uncased = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\bio_uncased_cbow.bin"
    #ruta_bio_skipgram_uncased = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\bio_uncased_skipgram.bin"
    #model_bio_cbow_uncased = fasttext.load_model(ruta_bio_cbow_uncased)
    #model_bio_skipgram_uncased = fasttext.load_model(ruta_bio_skipgram_uncased)

    #ruta_clinic_cbow_cased = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\clinic_cased_cbow.bin"
    #ruta_clinic_skipgram_cased = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\clinic_cased_skipgram.bin"
    #model_clinic_cbow_cased = fasttext.load_model(ruta_clinic_cbow_cased)
    #model_clinic_skipgram_cased = fasttext.load_model(ruta_clinic_skipgram_cased)

    #ruta_clinic_cbow_uncased = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\clinic_uncased_cbow.bin"
    #ruta_clinic_skipgram_uncased = str(os.path.abspath(os.getcwd())) + "\\ModelBin\\clinic_uncased_skipgram.bin"
    #model_clinic_cbow_uncased = fasttext.load_model(ruta_clinic_cbow_uncased)
    #model_clinic_skipgram_uncased = fasttext.load_model(ruta_clinic_skipgram_uncased)

        #Loop para vectorizar y guardar en diccionario
    for key in dict_notas_sin_vector.keys():
        lista_palabras_vectorizadas=[]
        dict_iterador.clear()

        dict_iterador=dict_notas_sin_vector[key].copy()
        parrafo_inicial = str(dict_iterador['interrogatorio_inicial'])
        parrafo_final = str(dict_iterador['interrogatorio_final'])

        result_tokens_incial=clean_tokens(parrafo_inicial)
        result_tokens_final = clean_tokens(parrafo_final)

        tokens_inicial = result_tokens_incial[0]
        tokens_final = result_tokens_final[0]

        tokens_frec_inicial = result_tokens_incial[1]
        tokens_frec_final = result_tokens_final[1]

        dict_iterador['tokens_inicial'] = tokens_inicial.copy()
        dict_iterador['tokens_final'] = tokens_final.copy()

        dict_iterador['tokens_frec_inicial'] = tokens_frec_inicial.copy()
        dict_iterador['tokens_frec_final'] = tokens_frec_final.copy()

        #Vectorizacion de parablas con Biomedical Cased CBOW-----------------------------------------------------------
        for word in tokens_inicial:
            #Promedio del vector de palabra de 300 datos
            valor_palabra=np.mean(model_bio_cbow_cased.get_word_vector(word))
            lista_palabras_vectorizadas.append(valor_palabra)
        dict_iterador['Biomedical_Cased_CBOW_inicial'] = lista_palabras_vectorizadas.copy()
        lista_palabras_vectorizadas.clear()

        for word in tokens_final:
            #Promedio del vector de palabra de 300 datos
            valor_palabra=np.mean(model_bio_cbow_cased.get_word_vector(word))
            lista_palabras_vectorizadas.append(valor_palabra)
        dict_iterador['Biomedical_Cased_CBOW_final'] = lista_palabras_vectorizadas.copy()
        lista_palabras_vectorizadas.clear()

        #Vectorizacion de parablas con Biomedical Cased SKIPGRAM--------------------------------------------------------
#        for word in tokens_inicial:
#            #Promedio del vector de palabra de 300 datos
#            valor_palabra=np.mean(model_bio_skipgram_cased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Biomedical_Cased_SKIPGRAM_inicial'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

#        for word in tokens_final:
#            #Promedio del vector de palabra de 300 datos
#            valor_palabra=np.mean(model_bio_skipgram_cased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Biomedical_Cased_SKIPGRAM_final'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

        # Vectorizacion de parablas con Biomedical Uncased CBOW-----------------------------------------------------------
#        for word in tokens_inicial:
#            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_bio_cbow_uncased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Biomedical_Uncased_CBOW_inicial'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

#        for word in tokens_final:
            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_bio_cbow_uncased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Biomedical_Uncased_CBOW_final'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

        # Vectorizacion de parablas con Biomedical Uncased SKIPGRAM--------------------------------------------------------
#        for word in tokens_inicial:
            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_bio_skipgram_uncased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Biomedical_Uncased_SKIPGRAM_inicial'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

#        for word in tokens_final:
#            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_bio_skipgram_uncased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Biomedical_Uncased_SKIPGRAM_final'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()


        #*************************CLINIC********************************************************************************

        # Vectorizacion de parablas con Clinic Cased CBOW-----------------------------------------------------------
#        for word in tokens_inicial:
#            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_clinic_cbow_cased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Clinic_Cased_CBOW_inicial'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

#        for word in tokens_final:
            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_clinic_cbow_cased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Clinic_Cased_CBOW_final'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

        # Vectorizacion de parablas con Clinic Cased SKIPGRAM--------------------------------------------------------
#        for word in tokens_inicial:
#            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_clinic_skipgram_cased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Clinic_Cased_SKIPGRAM_inicial'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

#        for word in tokens_final:
            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_clinic_skipgram_cased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Clinic_Cased_SKIPGRAM_final'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

        # Vectorizacion de parablas con Clinic Uncased CBOW-----------------------------------------------------------
#        for word in tokens_inicial:
            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_clinic_cbow_uncased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Clinic_Uncased_CBOW_inicial'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

#        for word in tokens_final:
            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_clinic_cbow_uncased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Clinic_Uncased_CBOW_final'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

        # Vectorizacion de parablas con Clinic Uncased SKIPGRAM--------------------------------------------------------
#        for word in tokens_inicial:
            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_clinic_skipgram_uncased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Clinic_Uncased_SKIPGRAM_inicial'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

#        for word in tokens_final:
            # Promedio del vector de palabra de 300 datos
#            valor_palabra = np.mean(model_clinic_skipgram_uncased.get_word_vector(word))
#            lista_palabras_vectorizadas.append(valor_palabra)
#        dict_iterador['Clinic_Uncased_SKIPGRAM_final'] = lista_palabras_vectorizadas.copy()
#        lista_palabras_vectorizadas.clear()

        dict_WE_vector[key] = dict_iterador.copy()

    #Agregar Resumen Tokens y Matriz Embebido Biomedical Cased CBOW
    df = pd.DataFrame(data=dict_WE_vector)
    serie_tokens_inicial = df.loc["tokens_inicial"]
    serie_tokens_final = df.loc["tokens_final"]

    #Lista de Tokens interrogatorio Final
    list_total_tokens_inicial=list(itertools.chain.from_iterable(serie_tokens_inicial.tolist()))
    list_total_tokens_final=list(itertools.chain.from_iterable(serie_tokens_final.tolist()))

    list_uniques_tokens_inicial = list(dict.fromkeys(list_total_tokens_inicial))
    list_uniques_tokens_final = list(dict.fromkeys(list_total_tokens_final))

    size_unique_tokens_inicial = len(list_uniques_tokens_inicial) + 1
    size_unique_tokens_final = len(list_uniques_tokens_final) + 1

    tokenizer_inicial = Tokenizer()
    tokenizer_inicial.fit_on_texts(list_uniques_tokens_inicial)
    word_index_inicial=tokenizer_inicial.word_index

    tokenizer_final = Tokenizer()
    tokenizer_final.fit_on_texts(list_uniques_tokens_final)
    word_index_final=tokenizer_final.word_index


    #BIO AND CLINIC CASED   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    weight_matrix_BIO_CBOW_Cased_inicial = np.zeros((size_unique_tokens_inicial, 300))
    weight_matrix_BIO_CBOW_Cased_final = np.zeros((size_unique_tokens_final, 300))

#    weight_matrix_BIO_SKIPGRAM_Cased_inicial = np.zeros((size_unique_tokens_inicial, 300))
#    weight_matrix_BIO_SKIPGRAM_Cased_final = np.zeros((size_unique_tokens_final, 300))

#    weight_matrix_CLIN_CBOW_Cased_inicial = np.zeros((size_unique_tokens_inicial, 300))
#    weight_matrix_CLIN_CBOW_Cased_final = np.zeros((size_unique_tokens_final, 300))

#    weight_matrix_CLIN_SKIPGRAM_Cased_inicial = np.zeros((size_unique_tokens_inicial, 300))
#    weight_matrix_CLIN_SKIPGRAM_Cased_final = np.zeros((size_unique_tokens_final, 300))

    #BIO AND CLINIC UNCASED----------------------------------------------------------
#    weight_matrix_BIO_CBOW_Uncased_inicial = np.zeros((size_unique_tokens_inicial, 300))
#    weight_matrix_BIO_CBOW_Uncased_final = np.zeros((size_unique_tokens_final, 300))

#    weight_matrix_BIO_SKIPGRAM_Uncased_inicial = np.zeros((size_unique_tokens_inicial, 300))
#    weight_matrix_BIO_SKIPGRAM_Uncased_final = np.zeros((size_unique_tokens_final, 300))

#    weight_matrix_CLIN_CBOW_Uncased_inicial = np.zeros((size_unique_tokens_inicial, 300))
#    weight_matrix_CLIN_CBOW_Uncased_final = np.zeros((size_unique_tokens_final, 300))

#    weight_matrix_CLIN_SKIPGRAM_Uncased_inicial = np.zeros((size_unique_tokens_inicial, 300))
#    weight_matrix_CLIN_SKIPGRAM_Uncased_final = np.zeros((size_unique_tokens_final, 300))

    for word, i in word_index_inicial.items():

        vector_bio_cbow_cased = model_bio_cbow_cased.get_word_vector(word)
#        vector_bio_skipgram_cased = model_bio_skipgram_cased.get_word_vector(word)

#        vector_clin_cbow_cased = model_clinic_cbow_cased.get_word_vector(word)
#        vector_clin_skipgram_cased = model_clinic_skipgram_cased.get_word_vector(word)

#        vector_bio_cbow_uncased = model_bio_cbow_uncased.get_word_vector(word)
#        vector_bio_skipgram_uncased = model_bio_skipgram_uncased.get_word_vector(word)

#        vector_clin_cbow_uncased = model_clinic_cbow_uncased.get_word_vector(word)
#        vector_clin_skipgram_uncased = model_clinic_skipgram_uncased.get_word_vector(word)

        if vector_bio_cbow_cased is not None:
            weight_matrix_BIO_CBOW_Cased_inicial[i] = vector_bio_cbow_cased
#        if vector_bio_skipgram_cased is not None:
#            weight_matrix_BIO_SKIPGRAM_Cased_inicial[i] = vector_bio_skipgram_cased

#        if vector_clin_cbow_cased is not None:
#            weight_matrix_CLIN_CBOW_Cased_inicial[i] = vector_clin_cbow_cased
#        if vector_clin_skipgram_cased is not None:
#            weight_matrix_CLIN_SKIPGRAM_Cased_inicial[i] = vector_clin_skipgram_cased

        #UNCASED
#        if vector_bio_cbow_uncased is not None:
#            weight_matrix_BIO_CBOW_Uncased_inicial[i] = vector_bio_cbow_uncased
#        if vector_bio_skipgram_uncased is not None:
#            weight_matrix_BIO_SKIPGRAM_Uncased_inicial[i] = vector_bio_skipgram_uncased

#        if vector_clin_cbow_uncased is not None:
#            weight_matrix_CLIN_CBOW_Uncased_inicial[i] = vector_clin_cbow_uncased
#        if vector_clin_skipgram_uncased is not None:
#            weight_matrix_CLIN_SKIPGRAM_Uncased_inicial[i] = vector_clin_skipgram_uncased


    for word, i in word_index_final.items():

        vector_bio_cbow_cased = model_bio_cbow_cased.get_word_vector(word)
#        vector_bio_skipgram_cased = model_bio_skipgram_cased.get_word_vector(word)

#        vector_clin_cbow_cased = model_clinic_cbow_cased.get_word_vector(word)
#        vector_clin_skipgram_cased = model_clinic_skipgram_cased.get_word_vector(word)

#        vector_bio_cbow_uncased = model_bio_cbow_uncased.get_word_vector(word)
#        vector_bio_skipgram_uncased = model_bio_skipgram_uncased.get_word_vector(word)

#        vector_clin_cbow_uncased = model_clinic_cbow_uncased.get_word_vector(word)
#        vector_clin_skipgram_uncased = model_clinic_skipgram_uncased.get_word_vector(word)

        if vector_bio_cbow_cased is not None:
            weight_matrix_BIO_CBOW_Cased_final[i] = vector_bio_cbow_cased
#        if vector_bio_skipgram_cased is not None:
#            weight_matrix_BIO_SKIPGRAM_Cased_final[i] = vector_bio_skipgram_cased

#        if vector_clin_cbow_cased is not None:
#            weight_matrix_CLIN_CBOW_Cased_final[i] = vector_clin_cbow_cased
#        if vector_clin_skipgram_cased is not None:
#            weight_matrix_CLIN_SKIPGRAM_Cased_final[i] = vector_clin_skipgram_cased

        # UNCASED
#        if vector_bio_cbow_uncased is not None:
#            weight_matrix_BIO_CBOW_Uncased_final[i] = vector_bio_cbow_uncased
#        if vector_bio_skipgram_uncased is not None:
#            weight_matrix_BIO_SKIPGRAM_Uncased_final[i] = vector_bio_skipgram_uncased

#        if vector_clin_cbow_uncased is not None:
#            weight_matrix_CLIN_CBOW_Uncased_final[i] = vector_clin_cbow_uncased
#        if vector_clin_skipgram_uncased is not None:
#            weight_matrix_CLIN_SKIPGRAM_Uncased_final[i] = vector_clin_skipgram_uncased


    dict_Resumen['tokens_all_inicial']=list_total_tokens_inicial.copy()
    dict_Resumen['tokens_all_final']=list_total_tokens_final.copy()

    dict_Resumen['tokens_unique_inicial']=list_uniques_tokens_inicial.copy()
    dict_Resumen['tokens_unique_final']=list_uniques_tokens_final.copy()

    dict_Resumen['tokens_size_inicial']=size_unique_tokens_inicial
    dict_Resumen['tokens_size_final']=size_unique_tokens_final

    #frecuencia de todos los tokens
    vocab_tokens_all_inicial=Counter()
    vocab_tokens_all_final=Counter()

    vocab_tokens_all_inicial.update(list_total_tokens_inicial.copy())
    vocab_tokens_all_final.update(list_total_tokens_final.copy())

    dict_Resumen['tokens_all_frec_inicial']=vocab_tokens_all_inicial.copy()
    dict_Resumen['tokens_all_frec_final']=vocab_tokens_all_final.copy()


    #CASED
    dict_Resumen['BIO_CBOW_Cased_embedding_layer_inicial']=weight_matrix_BIO_CBOW_Cased_inicial.copy()
    dict_Resumen['BIO_CBOW_Cased_embedding_layer_final']=weight_matrix_BIO_CBOW_Cased_final.copy()

#    dict_Resumen['BIO_SKIPGRAM_Cased_embedding_layer_inicial']=weight_matrix_BIO_SKIPGRAM_Cased_inicial.copy()
#    dict_Resumen['BIO_SKIPGRAM_Cased_embedding_layer_final']=weight_matrix_BIO_SKIPGRAM_Cased_final.copy()

#    dict_Resumen['CLIN_CBOW_Cased_embedding_layer_inicial']=weight_matrix_CLIN_CBOW_Cased_inicial.copy()
#    dict_Resumen['CLIN_CBOW_Cased_embedding_layer_final']=weight_matrix_CLIN_CBOW_Cased_final.copy()

#    dict_Resumen['CLIN_SKIPGRAM_Cased_embedding_layer_inicial']=weight_matrix_CLIN_SKIPGRAM_Cased_inicial.copy()
#    dict_Resumen['CLIN_SKIPGRAM_Cased_embedding_layer_final']=weight_matrix_CLIN_SKIPGRAM_Cased_final.copy()

    #UNCASED
#    dict_Resumen['BIO_CBOW_Uncased_embedding_layer_inicial']=weight_matrix_BIO_CBOW_Uncased_inicial.copy()
#    dict_Resumen['BIO_CBOW_Uncased_embedding_layer_final']=weight_matrix_BIO_CBOW_Uncased_final.copy()

#    dict_Resumen['BIO_SKIPGRAM_Uncased_embedding_layer_inicial']=weight_matrix_BIO_SKIPGRAM_Uncased_inicial.copy()
#    dict_Resumen['BIO_SKIPGRAM_Uncased_embedding_layer_final']=weight_matrix_BIO_SKIPGRAM_Uncased_final.copy()

#    dict_Resumen['CLIN_CBOW_Uncased_embedding_layer_inicial'] = weight_matrix_CLIN_CBOW_Uncased_inicial.copy()
#    dict_Resumen['CLIN_CBOW_Uncased_embedding_layer_final'] = weight_matrix_CLIN_CBOW_Uncased_final.copy()

#    dict_Resumen['CLIN_SKIPGRAM_Uncased_embedding_layer_inicial'] = weight_matrix_CLIN_SKIPGRAM_Uncased_inicial.copy()
#    dict_Resumen['CLIN_SKIPGRAM_Uncased_embedding_layer_final'] = weight_matrix_CLIN_SKIPGRAM_Uncased_final.copy()

    resultado.append(dict_WE_vector.copy())     #USO EN EL ANALISIS
    resultado.append(dict_Resumen.copy())
    return resultado