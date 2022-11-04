import re
import sys
import pandas as pd
import Funciones.SQLConnect as F_sql

#Auxiliar convertidor de resultado string a int____________________________________________________
def strToint(valor):
    resultado=None

    try:
        valor = re.sub('(\w+\.\w+)\.\w+', '\\1', valor)
    except:
        print('\n\tError con la estructura (2 puntos) de la variable')

    try:
        valor = re.sub('(\w+|\w+\.\w+)\/\w+\.*\w*', '\\1', valor)
    except:
        print('\n\tError con la estructura (diagonal) de la variable')

    try:
        valor = float(valor)
    except:
        print('\n\tError al convertir la variable a float')

    resultado=valor
    return resultado

#__________________________________________________________________________________________________

def structure_data_frame(extracted_data):
    print("\testructuracion de datos")
    listDict=[]
    dictResult={}
    TuplaInstancias=None
    valorKey=extracted_data[0]
    valorInstancias=extracted_data[1]

    for valor in valorKey:
        dictResult[str(valor)]=None


    for valor in valorInstancias:
        TuplaInstancias=valor
        for iteracion in range(len(TuplaInstancias)):
            dictResult[str(valorKey[iteracion])]=TuplaInstancias[iteracion]
        listDict.append(dictResult.copy())

    df = pd.DataFrame(columns=valorKey)
    for i in range(len(listDict)):
        #df = pd.DataFrame(listDict[i],index=[i])
        df = df.append(listDict[i], ignore_index=True)

    resultado=df
    return resultado

def structure_study_data_frame(extracted_data,listaDeterminacion):
    print("\testructuracion de datos de estudios de laboratorios")
    resultado=[]
    listDict=[]
    listDictFinal=[]
    listFolioDict=[]
    dictResult={}
    TuplaInstancias=None
    resultadoINT = None
    valorKey=extracted_data[0]
    valorInstancias=extracted_data[1]
    extendValorKey=[]

    #DataFrame en Blanco******************************************************************************
    extendValorKey=valorKey.copy()
    extendValorKey.extend(listaDeterminacion)

    df= pd.DataFrame(columns=extendValorKey)
    #*************************************************************************************************
    for valor in extendValorKey:
        dictResult[str(valor)]=None

    for valor in valorInstancias:
        TuplaInstancias=valor
        for iteracion in range(len(TuplaInstancias)):
            if valorKey[iteracion]=='resultado':
                resultadoINT=strToint(TuplaInstancias[iteracion])
                dictResult[str(valorKey[iteracion])] = resultadoINT
                dictResult[str(TuplaInstancias[iteracion-1])]=resultadoINT
                resultadoINT=None
            else:
                dictResult[str(valorKey[iteracion])] = TuplaInstancias[iteracion]

        listDict.append(dictResult.copy())
        dictResult = dictResult.fromkeys(dictResult, None)

    for i in range(len(listDict)):
        dictResult=listDict[i]
        folioDict=dictResult['folio_orden']
        for dict in listDict:
            if dict['folio_orden']==folioDict:
                dictResult[dict['determinacion']]=dict['resultado']

        if not folioDict in listFolioDict:
            listFolioDict.append(folioDict)
            listDictFinal.append(dictResult.copy())
        dictResult = dictResult.fromkeys(dictResult, None)

    for i in range(len(listDictFinal)):
        df = df.append(listDictFinal[i], ignore_index=True)
    df=df.drop(columns=['determinacion', 'resultado'])

    # Mover Columna DataFrame al final
    column_size = len(df.columns) - 1
    name_column = 'diagnostico_final'
    move_column = df.pop(name_column)

    df.insert(column_size, name_column, move_column)

    # Ordenar filas de menor a mayor con respecto a la columna "orden"
    df = df.sort_values(by=['nss'])

    # Verificacion de valores duplicados en columna 'orden'
    #dfDupli=df.duplicated(subset=['nss'], keep=False)

    # agrupamiento de valores repetidos donde se selecciona el maximo valor
    df2 = df.drop(columns=['folio_orden','fecha_orden','servicio_solicita'])
    try:
        #df2 = df2.groupby('nss').max()
        df2 = df2.groupby('nss',group_keys=True,dropna=False).min().reset_index()
    except OSError as err:
        print("\tOS error: {0}".format(err))
    except ValueError as e:
        print("\tERROR con el agrupamiento de datos\n\t".upper(), e)
    except:
        print("\tUnexpected error:", sys.exc_info()[0])
        raise


    #grouped = df.groupby("folio_orden").max('resultado').reset_index()
    #r=df.groupby(['nss','folio_orden']).max().reset_index()
    #r= df.groupby(by='folio_orden').max().reset_index()
    #s = df.groupby(by='folio_orden').sum()
    #t = df.groupby(by=['nss','folio_orden'], dropna=True).sum()


    resultado=[df,df2]
    return resultado

#-----------------------------------------------------------------------------------------------------------------
def extract_data_from_MYSQL(db_connection,destino):
    resultado = []
    print("\textracion de datos de mySQL: ",destino," ",db_connection)
    tabla_extraida=F_sql.extract_table_from_MYSQL(db_connection,destino)
    datos_estructurados=structure_data_frame(tabla_extraida)
    resultado=datos_estructurados

    return resultado

def join_data_from_MYSQL(db_connection,listSelect,listFrom,listOn,listWhere):
    resultado = []
    print("\tunion de datos de mySQL: ",listSelect,"\n\t",db_connection)
    tablas_unidas=F_sql.join_tables_MYSQL(db_connection,listSelect,listFrom,listOn,listWhere)
    datos_estructurados = structure_data_frame(tablas_unidas)
    resultado = datos_estructurados

    return resultado

def join_study_data_from_MYSQL(db_connection,listSelect,listFrom,listOn,study):
    resultado = []
    print("\tunion de datos de mySQL: ",listSelect,"\n\t",db_connection)
    lista_determinacion=F_sql.extract_determinacion_from_study_MYSQL(db_connection,study)
    tablas_unidas=F_sql.join_study_tables_MYSQL(db_connection,listSelect,listFrom,listOn,lista_determinacion)
    datos_estructurados = structure_data_frame(tablas_unidas)
    resultado = datos_estructurados

    return resultado

def join_valores_study_data_from_MYSQL(db_connection,listSelect,listFrom,listOn,study):
    resultado=[]
    print("\tunion de datos de mySQL: ",listSelect,"\n\t",db_connection)
    lista_determinacaion=F_sql.extract_determinacion_from_study_MYSQL(db_connection,study)
    tablas_unidas=F_sql.join_study_tables_MYSQL(db_connection,listSelect,listFrom,listOn,lista_determinacaion)
    datos_estructurados = structure_study_data_frame(tablas_unidas,lista_determinacaion)
    resultado = datos_estructurados
    return resultado

def join_multiple_study_data_from_MYSQL(db_connection,listStudies):
    print("\tunion de multiples estudios de mySQL: ", listStudies, "\n\t", db_connection)
    resultado=[]
    lista_determinacaion=[]
    lista_determinacaiones_totales=[]
    tablas_unidas_totales= [[],[]]

    for estudio in listStudies:
        listSelect = ['nota_inicial.*', 'laboratorio.folio_orden', 'laboratorio.fecha_orden',
                      'laboratorio.edad', 'laboratorio.servicio_solicita','nota_egreso.fecha_egreso',
                      estudio+'.determinacion',estudio+'.resultado','nota_egreso.diagnostico_final']
        listFrom = ['nota_inicial', 'laboratorio','nota_egreso', estudio]
        listOn = ['nota_inicial.nss=laboratorio.nss',
                  'nota_inicial.nss=nota_egreso.nss ',
                  'laboratorio.folio_orden='+estudio+'.folio_orden']

        lista_determinacaion=F_sql.extract_determinacion_from_study_MYSQL(db_connection,estudio)
        tablas_unidas = F_sql.join_study_tables_MYSQL(db_connection, listSelect, listFrom, listOn, lista_determinacaion)

        lista_determinacaiones_totales.extend(lista_determinacaion)
        tablas_unidas_totales[0]=tablas_unidas[0].copy()
        tablas_unidas_totales[1].extend(tablas_unidas[1].copy())

    datos_estructurados = structure_study_data_frame(tablas_unidas_totales,lista_determinacaiones_totales)
    resultado = datos_estructurados
    return resultado


def join_multiple_study_data_from_MYSQL_dxFinal(db_connection,listStudies,dx_final):
    print("\tunion de multiples estudios de mySQL: ", listStudies, "\n\t", db_connection)
    resultado=[]
    lista_determinacaion=[]
    lista_determinacaiones_totales=[]
    tablas_unidas_totales= [[],[]]

    for estudio in listStudies:
        listSelect = ['nota_inicial.*', 'laboratorio.folio_orden', 'laboratorio.fecha_orden',
                      'laboratorio.edad', 'laboratorio.servicio_solicita','nota_egreso.fecha_egreso',
                      estudio+'.determinacion',estudio+'.resultado','nota_egreso.diagnostico_final']
        listFrom = ['nota_inicial', 'laboratorio','nota_egreso', estudio]
        listOn = ['nota_inicial.nss=laboratorio.nss',
                  'nota_inicial.nss=nota_egreso.nss ',
                  'laboratorio.folio_orden='+estudio+'.folio_orden']

        lista_determinacaion=F_sql.extract_determinacion_from_study_MYSQL(db_connection,estudio)
        tablas_unidas = F_sql.join_study_tables_MYSQL_DXfinal(db_connection, listSelect, listFrom, listOn, lista_determinacaion,dx_final)

        lista_determinacaiones_totales.extend(lista_determinacaion)
        tablas_unidas_totales[0]=tablas_unidas[0].copy()
        tablas_unidas_totales[1].extend(tablas_unidas[1].copy())

    datos_estructurados = structure_study_data_frame(tablas_unidas_totales,lista_determinacaiones_totales)
    resultado = datos_estructurados
    return resultado

