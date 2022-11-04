import mysql.connector as sql

def closeDBconect(db_connection):
    db_connection.close()
    print("\tConexion Finalizada con MySQL".upper())
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
        print("\tConexion exitosa con base de Datos".upper(), db_connection)
        resultado=db_connection
    except sql.Error as e:
        print("\tError con la conexion con base de Datos".upper(), e)
    return (resultado)

#-----------------------------------------------------------------------------------------------------
def extract_table_from_MYSQL(db_connection,destino):
    print("\textracion de tabla de mySQL")
    resultado=None

    if db_connection.is_connected():
        db_cursor = db_connection.cursor()
    try:
        db_cursor.execute("select * from "+str(destino))
        instancias = db_cursor.fetchall()
        num_atributos = len(db_cursor.description)
        nombres_atributos = [i[0] for i in db_cursor.description]
        resultado=[nombres_atributos,instancias]

        db_connection.commit()
        print("\nConsulta JOIN a MYSQL exitoso...!")
    except sql.Error as e:
        print("\tERROR con la consulta de datos a MYSQL\n\t".upper(), e)
        db_connection.rollback()

    return resultado

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

def join_tables_MYSQL(db_connection,listSelect,listFrom,listOn,listWhere):
    print("\tunion de tablas de mySQL")
    strSelect=''
    query=''
    for valor in listSelect:
        if valor==listSelect[-1]:
            strSelect=strSelect+str(valor)
        else:
            strSelect = strSelect + str(valor)+", "

    if not listWhere:
        if len(listFrom)<=2:
            query='SELECT '+strSelect+" FROM "+str(listFrom[0])+' INNER JOIN '+str(listFrom[1])+' ON '+str(listOn[0])

    else:
        if len(listFrom)<=2:
            query='SELECT '+strSelect+" FROM "+str(listFrom[0])+' INNER JOIN '+str(listFrom[1])+' ON '+str(listOn[0])+' WHERE '+str(listWhere[0])
        else:
            query = 'SELECT ' + strSelect + " FROM " + str(listFrom[0])
            querySub=''
            for i in range(1,len(listFrom)):
                querySub =str(querySub)+' INNER JOIN ' + str(listFrom[i]) + ' ON ' + str(listOn[i-1])
            query = 'SELECT ' + strSelect + " FROM " + str(listFrom[0])+str(querySub)+' WHERE '+str(listWhere[0])

    print(query)

    if db_connection.is_connected():
        db_cursor = db_connection.cursor()
    try:
        db_cursor.execute(query)
        instancias = db_cursor.fetchall()
        num_atributos = len(db_cursor.description)
        nombres_atributos = [i[0] for i in db_cursor.description]
        resultado=[nombres_atributos,instancias]

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

def join_study_tables_MYSQL_DXfinal (db_connection,listSelect,listFrom,listOn,listDeterminacion,dxFinal):
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
        query = 'SELECT ' + strSelect + " FROM " + str(listFrom[0]) + str(querySub) + ' WHERE diagnostico_final =\''+str(dxFinal) +'\' AND '+ str(strWhere)

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