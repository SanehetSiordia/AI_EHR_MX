import mysql.connector as sql
import Funciones.data_organize as dataO

def closeDBconect(db_connection):
    db_connection.close()
    print("\n\tConexion Finalizada con MySQL".upper())
    return None

def openDBconect(propiedadesUsuario):
    resultado=None
    BDexist=0
    db_connection = None        # Variable conector SQL con base de datos
    host_user = propiedadesUsuario[0]
    usuario = propiedadesUsuario[1]
    contra = propiedadesUsuario[2]
    dbName= propiedadesUsuario[3]

    #Establecer Conexion --------------------------------------------------------------------
    try:
        db_connection = sql.connect(
            host=host_user,
            user=usuario,
            passwd=contra,
            database=dbName
        )
        print("\n\tConexion exitosa con base de Datos".upper(), db_connection)
        resultado=db_connection
    except sql.Error as e:
        print("\n\tError con la conexion con base de Datos".upper(), e)
    return (resultado)

#______________________________________________________________________________________________________________________
def extract_determinacion_from_study_MYSQL(db_connection,destino):
    print('\textracion de valores de determinacion del estudio: ',str(destino))
    resultado=[]

    query='select determinacion from '+destino+' group by determinacion'

    if db_connection.is_connected():
        db_cursor = db_connection.cursor()
    try:
        db_cursor.execute(query)
        instancias = db_cursor.fetchall()
        nombres_atributos = [i[0] for i in db_cursor.description]
        for i in range(len(instancias)):
            resultado.append(instancias[i][0])

        db_connection.commit()
        print("\nConsulta JOIN a MYSQL exitoso...!")
    except sql.Error as e:
        print("\tERROR con la consulta de datos a MYSQL\n\t".upper(), e)
        db_connection.rollback()

    return resultado

def join_study_tables_MYSQL(db_connection,listSelect,listFrom,listOn,listDeterminacion):
    print("\tunion de tablas de estudios de mySQL")
    resultado=[]
    strSelect=''
    query=''
    strDeterminacion=''
    strWhere='determinacion='+str(strDeterminacion)

    for valor in listSelect:
        if valor==listSelect[-1]:
            strSelect=strSelect+str(valor)
        else:
            strSelect = strSelect + str(valor)+", "

    for i in range(len(listDeterminacion)):
        query = 'SELECT ' + strSelect + " FROM " + str(listFrom[0])
        querySub = ''
        strWhere=''

        for j in range(1, len(listFrom)):
            querySub = str(querySub) + ' INNER JOIN ' + str(listFrom[j]) + ' ON ' + str(listOn[j - 1])

        strWhere = 'determinacion=\'' + str(listDeterminacion[i])+'\''
        query = 'SELECT ' + strSelect + " FROM " + str(listFrom[0]) + str(querySub) + ' WHERE ' + str(strWhere)

        print(query)

        if db_connection.is_connected():
            db_cursor = db_connection.cursor()

        if i==0:
            try:
                db_cursor.execute(query)
                instancias = db_cursor.fetchall()
                num_atributos = len(db_cursor.description)
                nombres_atributos = [i[0] for i in db_cursor.description]
                resultado=[nombres_atributos,instancias]
                db_connection.commit()
                print("\nConsulta JOIN de MYSQL exitoso para itereacion: ",i," con determinacion: ",listDeterminacion[i])
            except sql.Error as e:
                print("\tERROR con la consulta de datos a MYSQL\n\t".upper(), e)
                db_connection.rollback()
        else:
            try:
                db_cursor.execute(query)
                Subinstancias = db_cursor.fetchall()
                instancias.extend(Subinstancias)
                num_atributos = len(db_cursor.description)
                nombres_atributos = [i[0] for i in db_cursor.description]
                resultado=[nombres_atributos,instancias]
                db_connection.commit()
                print("\nConsulta JOIN de MYSQL exitoso para itereacion: ",i," con determinacion: ",listDeterminacion[i])
            except sql.Error as e:
                print("\tERROR con la consulta de datos a MYSQL\n\t".upper(), e)
                db_connection.rollback()

    return resultado

def join_multiple_study_data_from_MYSQL(db_connection,listStudies):
    print("\tunion de multiples estudios de mySQL: ", listStudies, "\n\t", db_connection)
    resultado=[]
    lista_determinacaion=[]
    lista_determinacaiones_totales=[]
    tablas_unidas_totales= [[],[]]

    for estudio in listStudies:
        listSelect = ['nota_inicial.nss','nota_inicial.genero','nota_inicial.peso','nota_inicial.talla','nota_inicial.temperatura',
                      'nota_inicial.frec_respiratoria','nota_inicial.frec_cardiaca','nota_inicial.pres_arterial','nota_inicial.imc',
                      'nota_inicial.saturacion','nota_inicial.glc_capilar','laboratorio.folio_orden',
                      estudio+'.determinacion',estudio+'.resultado','nota_egreso.diagnostico_final']

        listFrom = ['nota_inicial', 'laboratorio','nota_egreso', estudio]
        listOn = ['nota_inicial.nss=laboratorio.nss',
                  'nota_inicial.nss=nota_egreso.nss ',
                  'laboratorio.folio_orden='+estudio+'.folio_orden']

        lista_determinacaion=extract_determinacion_from_study_MYSQL(db_connection,estudio)
        tablas_unidas = join_study_tables_MYSQL(db_connection, listSelect, listFrom, listOn, lista_determinacaion)

        lista_determinacaiones_totales.extend(lista_determinacaion)
        tablas_unidas_totales[0]=tablas_unidas[0].copy()
        tablas_unidas_totales[1].extend(tablas_unidas[1].copy())

    datos_estructurados = dataO.structure_study_data_frame(tablas_unidas_totales,lista_determinacaiones_totales)
    resultado = datos_estructurados
    return resultado
#______________________________________________________________________________________________________________________









def recolectar_datos(db_conexion):
    resultado=None

    query='SELECT nota_inicial.nss AS \'nss_ingreso\', nota_inicial.diagnostico_inicial, nota_egreso.diagnostico_final, nota_inicial.genero, nota_inicial.interrogatorio AS \'interrogatorio_inicial\', nota_egreso.resumen_evolucion AS \'interrogatorio_final\' FROM nota_inicial INNER JOIN laboratorio ON nota_inicial.nss=laboratorio.nss INNER JOIN nota_egreso ON nota_inicial.nss=nota_egreso.nss WHERE diagnostico_final=\'embolia\' OR diagnostico_final=\'neumonia\' OR diagnostico_final=\'control\' GROUP BY nota_inicial.nss ORDER BY diagnostico_final'

    if db_conexion.is_connected():
        db_cursor = db_conexion.cursor()
    try:
        db_cursor.execute(query)
        instancias = db_cursor.fetchall()
        num_atributos = len(db_cursor.description)
        nombres_atributos = [i[0] for i in db_cursor.description]
        resultado = [nombres_atributos, instancias]
        db_conexion.commit()
        print('\n\tConsulta JOIN de MYSQL exitoso')
    except sql.Error as e:
        print('\n\tERROR con la consulta de datos a MYSQL\n\t'.upper(), e)
        db_conexion.rollback()

    return resultado


def recolectar_labs(db_conexion):
    resultado= None
    ListEstudios = ['hematologia', 'coagulaciones', 'inmuno_infecto', 'inmunologia', 'quimica_clinica']

    if db_conexion.is_connected():
        try:
            datalab_raw = join_multiple_study_data_from_MYSQL(db_conexion,ListEstudios)
            db_conexion.commit()
            print('\n\tConsulta JOIN de MYSQL exitoso')
        except sql.Error as e:
            print('\n\tERROR con la consulta de datos a MYSQL\n\t'.upper(), e)
            db_conexion.rollback()

    print('recoleccion de laboratorios clinicos')
    resultado=datalab_raw
    return resultado