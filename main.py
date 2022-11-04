import Funciones.PDFSupports as pdfSupports
import Funciones.PDFWorks as pdfWorks
import Funciones.SQLconnect as sqlconnect

def main():
    answer = None
    answerFolder=None
    answerEval=None
    rutasCarpetas = pdfSupports.rutasCarpetas()

    # PARTE 1: Evaluacion de carpetas y Contenido de PDFS-----------------------------------------------------------------------
    print('Obtencion de rutas de carpetas'.upper())

    # 1.2-Preguntar si hay archivos PDFs pendientes para evaluar
    while True:
        answer=input("\n¿Quiere organizar archivos PDFs pendientes?\n1-Si\n2-No\nRespuesta: ")
        if answer.isdigit():
            try:
                answer = int(answer)
                if answer >= 1 and answer <= 2:
                    break
                else:
                    print("\nError, Favor de seleccionar la opciones disponibles".upper())
            except ValueError:
                print("\nError, Favor de seleccionar la opciones disponibles".upper())
        else:
            print("\nError, Favor de seleccionar la opciones disponibles".upper())

    if answer == 1:
        print("\n\tSe Organizaran PDFs Pendientes")
        pdfsParaEvaluar=pdfWorks.pdfsPendientes(rutasCarpetas[1][6])
        #1.3-Organizar cada PDF pendiente (si hay)
        if pdfsParaEvaluar[0]>0:
            for evalRutaPDF in pdfsParaEvaluar[1]:
                pdfWorks.pdfsOrganizar(rutasCarpetas[0][0],rutasCarpetas[1],rutasCarpetas[2],evalRutaPDF)
        else:
            print("No hay archivos pdfs pendientes a organizar\n")
    else:
        print('Accion Cancelada'.upper())

    #PARTE 2: Leer y crear diccionarios para ser registrados en base de datos.---------------------------------------------
    #2.1-Preguntar si se desea evaluar pdfs en carpetas importantes
    answer=None
    while True:
        answer=input("\n¿Quiere evaluar archivos PDFs existentes?\n1-Si\n2-No\nRespuesta: ")
        if answer.isdigit():
            try:
                answer = int(answer)
                if answer >= 1 and answer <= 2:
                    break
                else:
                    print("\nError, Favor de seleccionar la opciones disponibles".upper())
            except ValueError:
                print("\nError, Favor de seleccionar la opciones disponibles".upper())
        else:
            print("\nError, Favor de seleccionar la opciones disponibles".upper())

    if answer == 1:
        while True:
            answerFolder = input("\n\t¿Cual Carpeta Requiere Evaluar?\n\t"
                           "1-Pacientes|Notas Clinicas\n\t"
                           "2-Laboratorios\n\t"
                           "3-Notas de Egreso\n\t"      
                           "0-Cancelar|Salir\n\t"
                           "Respuesta: ")
            if answerFolder.isdigit():
                try:
                    answerFolder = int(answerFolder)
                    if answerFolder >= 0 and answerFolder <= 3:
                        break
                    else:
                        print("\n\tError, Favor de seleccionar la opciones disponibles".upper())
                except ValueError:
                    print("\n\tError, Favor de seleccionar la opciones disponibles".upper())
            else:
                print("\n\tError, Favor de seleccionar la opciones disponibles".upper())

        while True:
            answerEval = input("\n\t\t¿Desea evaluar todos los archivos o los inexistentes en la base de datos?\n\t\t"
                           "1-Todos los Archivos\n\t\t"
                           "2-Inexistentes en la Base de Datos\n\t\t"
                           "0-Cancelar|Salir\n\t\t"
                           "Respuesta: ")
            if answerEval.isdigit():
                try:
                    answerEval = int(answerEval)
                    if answerEval >= 0 and answerEval <= 2:
                        break
                    else:
                        print("\n\t\tError, Favor de seleccionar la opciones disponibles".upper())
                except ValueError:
                    print("\n\t\tError, Favor de seleccionar la opciones disponibles".upper())
            else:
                print("\n\t\tError, Favor de seleccionar la opciones disponibles".upper())

    else:
        print('Accion Cancelada'.upper())

    if answerFolder==1 and answerEval==1:
        print('\n\t\tSe evaluaran TODOS LOS ARCHIVOS de Pacientes|Notas Clinicas')
        archivos_en_bd = []
        dicPacientes_NotaInicial=pdfWorks.pdfsNotaInicial(rutasCarpetas[0][0],rutasCarpetas[1][1],rutasCarpetas[1][5],archivos_en_bd)

        #Guardar diccionario en pickle para consulta rapida
        pdfSupports.pickleGuardarDic(dicPacientes_NotaInicial[0],'Pacientes')
        pdfSupports.pickleGuardarDic(dicPacientes_NotaInicial[1],'NotaInicial')
        print('\n\t\tFin de evaluacion Pacientes|Notas Clinicas'.upper())

    elif answerFolder==2 and answerEval==1:
        print('\n\t\tSe evaluaran TODOS LOS ARCHIVOS de Laboratorios')
        archivos_en_bd=[]
        dicPacientes_Laboratorio = pdfWorks.pdfsLaboratorio(rutasCarpetas[0][0], rutasCarpetas[1][4],rutasCarpetas[1][5],archivos_en_bd)

        #Guardar diccionario en pickle para consulta rapida
        pdfSupports.pickleGuardarDic(dicPacientes_Laboratorio,'Laboratorio')
        print('\n\t\tFin de evaluacion Laboratorios'.upper())


    elif answerFolder==3 and answerEval==1:      #NOTAS DE EGRESO 04/05/2021--------------------------------------------
        print('\n\t\tSe evaluaran TODOS LOS ARCHIVOS de Notas de Egreso')
        archivos_en_bd=[]
        dicPacientes_NotaEgreso = pdfWorks.pdfsNotaEgreso(rutasCarpetas[0][0], rutasCarpetas[1][3],rutasCarpetas[1][5],archivos_en_bd)

        #Guardar diccionario en pickle para consulta rapida
        pdfSupports.pickleGuardarDic(dicPacientes_NotaEgreso,'NotaEgreso')
        print('\n\t\tFin de evaluacion Laboratorios'.upper())

    elif answerFolder==1 and answerEval==2:
        print('\n\t\tSe evaluaran ARCHIVOS INEXISTENTES en BD de Pacientes|Notas Clinicas')
        nombreTabla='nota_inicial'

        #CONEXION CON MYSQL
        archivos_en_bd=sqlconnect.DBStatusTables(nombreTabla)

        #Creacion de diccionario para Pickle
        dicPacientes_NotaInicial=pdfWorks.pdfsNotaInicial(rutasCarpetas[0][0],rutasCarpetas[1][1],rutasCarpetas[1][5],archivos_en_bd)

        #Guardar diccionario en pickle para consulta rapida
        pdfSupports.pickleGuardarDic(dicPacientes_NotaInicial[0],'Pacientes')
        pdfSupports.pickleGuardarDic(dicPacientes_NotaInicial[1],'NotaInicial')
        print('\n\t\tFin de evaluacion Pacientes|Notas Clinicas'.upper())

    elif answerFolder == 2 and answerEval == 2:
        print('\n\t\tSe evaluaran ARCHIVOS INEXISTENTES en BD de Laboratorios')
        nombreTabla = 'laboratorio'

        # CONEXION CON MYSQL
        archivos_en_bd=sqlconnect.DBStatusTables(nombreTabla)

        #Creacion de diccionario para Pickle
        dicPacientes_Laboratorio = pdfWorks.pdfsLaboratorio(rutasCarpetas[0][0], rutasCarpetas[1][4],rutasCarpetas[1][5],archivos_en_bd)

        #Guardar diccionario en pickle para consulta rapida
        pdfSupports.pickleGuardarDic(dicPacientes_Laboratorio,'Laboratorio')
        print('\n\t\tFin de evaluacion Laboratorios'.upper())

    elif answerFolder == 3 and answerEval == 2:  #NOTAS DE EGRESO 04/05/2021--------------------------------------------
        print('\n\t\tSe evaluaran ARCHIVOS INEXISTENTES en BD de Notas de Egreso')
        nombreTabla = 'nota_egreso'

        # CONEXION CON MYSQL
        archivos_en_bd=sqlconnect.DBStatusTables(nombreTabla)

        #Creacion de diccionario para Pickle
        dicPacientes_NotaEgreso = pdfWorks.pdfsNotaEgreso(rutasCarpetas[0][0], rutasCarpetas[1][3],rutasCarpetas[1][5],archivos_en_bd)

        #Guardar diccionario en pickle para consulta rapida
        pdfSupports.pickleGuardarDic(dicPacientes_NotaEgreso,'NotaEgreso')
        print('\n\t\tFin de evaluacion Notas de Egreso'.upper())

    elif answerFolder==0 or answerEval==0:
        print('Accion Cancelada'.upper())

    # PARTE 3: Interacion con BASE DE DATOS-------------------------------------------------------------------------------------------------------------
    answer = None

    while True:
        answer = input("\n¿Quiere cargar datos a la Base de Datos?\n1-Si\n2-No\nRespuesta: ")
        if answer.isdigit():
            try:
                answer = int(answer)
                if answer >= 1 and answer <= 2:
                    break
                else:
                    print("\nError, Favor de seleccionar la opciones disponibles".upper())
            except ValueError:
                print("\nError, Favor de seleccionar la opciones disponibles".upper())
        else:
            print("\nError, Favor de seleccionar la opciones disponibles".upper())
    if answer == 1:
        #3.1-Cargar diccionarios de Pickle
        print("\n\tSe cargaran datos del PICKLE a BASE DE DATOS")
        pickleDiccionarios = pdfSupports.pickleCargarDic(rutasCarpetas[0][0])
        print('\tDiccionarios desde Pickle')

        #3.2-Consultar a BASE DE DATOS
        sqlconnect.DBmanager(pickleDiccionarios)                   #Agregar opcion de llenado a base de datos
    else:
        print('Accion Cancelada'.upper())



    print('\tADIOS...! :3')
    return None

main()