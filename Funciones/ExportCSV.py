import os


def export_dataframe_to_csv(listDF,nombre):
    df=listDF[0]
    df2=listDF[1]
    print("\texportar datos a csv")
    resultado=None

    rutaActual = os.path.abspath(os.getcwd())

    df.to_csv(str(rutaActual)+'\\Archivos_CSV\\'+'\\1_Completos\\'+str(nombre)+'.csv', index=False, header=True)
    df2.to_csv(str(rutaActual)+'\\Archivos_CSV\\'+'\\2_Editados\\'+str(nombre)+'_EDIT.csv', index=False, header=True)

    return resultado