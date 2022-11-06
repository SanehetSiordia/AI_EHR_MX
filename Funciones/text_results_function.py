import os
import re

def save_best_result(valores,nombre):
    resultado=None
    list_txt=[]
    #Contar Documentos tipo Texto
    #ruta=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    ruta= os.path.abspath(os.getcwd())
    ruta=str(ruta)+'\\ResultsText'
    contenido = os.listdir(ruta)

    list_txt = [x for x in contenido if x.startswith('Best_') and x.endswith('.txt')]

    nombre=str(nombre)+str(len(list_txt)+1)
    print(nombre)

    texto = 'Resultados para '+ str(nombre)+'\n'
    for x in valores:
        texto=str(texto)+str(x)+'\n'

    texto=texto.replace('(','').replace(')','').replace('\'','').replace(',',':')

    f = open(str(ruta)+'\\'+str(nombre)+'.txt', 'w+')
    f.write(str(texto))
    f.close()

    return resultado

def save_prom_result(valores,nombre):
    resultado=None
    list_txt = []
    # Contar Documentos tipo Texto
    # ruta=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    ruta = os.path.abspath(os.getcwd())
    ruta = str(ruta) + '\\ResultsText'
    contenido = os.listdir(ruta)

    list_txt = [x for x in contenido if x.startswith('Prom_') and x.endswith('.txt')]

    nombre = str(nombre) + str(len(list_txt) + 1)
    print(nombre)

    texto = 'Resultados para '+ str(nombre)+'\n'
    for x in valores:
        texto = str(texto) + str(x) + '\n'

    texto = texto.replace('(', '').replace(')', '').replace('\'', '').replace(',', ':')

    f = open(str(ruta) + '\\' + str(nombre) + '.txt', 'w+')
    f.write(str(texto))
    f.close()

    return resultado

def save_val_result(valores,nombre):
    resultado=None
    list_txt=[]
    #Contar Documentos tipo Texto
    #ruta=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    ruta= os.path.abspath(os.getcwd())
    ruta=str(ruta)+'\\ResultsText'
    contenido = os.listdir(ruta)

    list_txt = [x for x in contenido if x.startswith('Val_') and x.endswith('.txt')]

    nombre=str(nombre)+str(len(list_txt)+1)
    print(nombre)

    texto = 'Resultados para '+ str(nombre)+'\n'
    for x in valores:
        texto=str(texto)+str(x)+'\n'

    texto=texto.replace('(','').replace(')','').replace('\'','').replace(',',':')

    f = open(str(ruta)+'\\'+str(nombre)+'.txt', 'w+')
    f.write(str(texto))
    f.close()

    return resultado

def save_best_param(valores,nombre,WE,start,final):
    resultado=None
    list_txt = []
    # Contar Documentos tipo Texto
    # ruta=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    ruta = os.path.abspath(os.getcwd())
    ruta = str(ruta) + '\\ResultsText'
    contenido = os.listdir(ruta)

    list_txt = [x for x in contenido if x.startswith('Param_best') and x.endswith('.txt')]

    nombre = str(nombre) + str(len(list_txt) + 1)
    print(nombre)

    texto = 'Resultados para ' + str(nombre) +'\nWord Embedding: '+str(WE)+'\nTiempo Inicial: '+str(start)+'\nTiempo Final: '+str(final)+'\n'

    for key in valores:
        texto = str(texto) + '\n' + str(key) + ' : ' + str(valores[key])

    f = open(str(ruta) + '\\' + str(nombre) + '.txt', 'w+')
    f.write(str(texto))
    f.close()

    return resultado

def save_result_param(valores,nombre,WE,start,final):
    resultado=None
    list_txt = []
    # Contar Documentos tipo Texto
    # ruta=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    ruta = os.path.abspath(os.getcwd())
    ruta = str(ruta) + '\\ResultsText'
    contenido = os.listdir(ruta)

    list_txt = [x for x in contenido if x.startswith('Param_result') and x.endswith('.txt')]

    nombre = str(nombre) + str(len(list_txt) + 1)
    print(nombre)

    texto = 'Resultados para ' + str(nombre) +'\nWord Embedding: '+str(WE)+'\nTiempo Inicial: '+str(start)+'\nTiempo Final: '+str(final)+'\n'

    for key in valores:
        texto = str(texto) + '\n' + str(key) + ' : ' + str(valores[key])

    f = open(str(ruta) + '\\' + str(nombre) + '.txt', 'w+')
    f.write(str(texto))
    f.close()

    return resultado