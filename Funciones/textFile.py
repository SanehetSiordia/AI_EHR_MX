import os

def text_file(texto,nombre):
    resultado=None
    ruta= os.path.abspath(os.getcwd())
    ruta=str(ruta)+'\\Txt_Result'

    f = open(str(ruta)+'\\'+str(nombre)+'.txt', 'w+')
    f.write(str(texto))
    f.close()

    return resultado