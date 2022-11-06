from datetime import datetime
import Funciones.sql_connection as sql
import Funciones.pickle_function as pickle
import Funciones.ExportCsv as expcsv
import Funciones.dictionary_function as dict
import Funciones.text_results_function as textR
import Funciones.word_embedding_fasttext as wordE
import Funciones.data_organize as dataOrganize
import Funciones.BILSTM_function as BILSTMmodel


def main():
    salir = False

    while True:
        answer = input("\nFAVOR DE SELECCIONAR UNA OPCION\n\t"
                       "1-GENERAR WORDS EMBEDDING Y LABS INPUT\n\t"
                       "2-CARGAR WORDS EMBEDDING\n\t"
                       "3-EXPORTAR WORDS EMBEDDING.csv\n\t"
                       "4-CARGAR Y UNIR WE+LABS\n\t"
                       "0-CANCELAR/SALIR\n\tRESPUESTA: ")

        if answer.isdigit():
            try:
                answer = int(answer)
                if answer >= 0 and answer <= 4:
                    break
                else:
                    print("\nError, Favor de seleccionar la opciones disponibles".upper())
            except ValueError:
                print("\nError, Favor de seleccionar la opciones disponibles".upper())
        else:
            print("\nError, Favor de seleccionar la opciones disponibles".upper())


    if answer == 1:

        diccionario_notas_sin_datos = {}
        diccionario_notas_sin_vector = {}
        diccionario_notas_con_vector = {}

        diccionario_notas_sin_datos = dict.setDictNotasClinicas()

        # Recoleccion de interrogatorios
        conexion_db = sql.openDBconect(
            propiedadesUsuario=["localhost", "root", "MySQLRootPass2021", "enfermedadesrespiratorias"])
        datos_mysql = sql.recolectar_datos(conexion_db)
        sql.closeDBconect(conexion_db)

        diccionario_notas_sin_vector = dict.guardarDictNotasClinicas(datos_mysql, diccionario_notas_sin_datos)

        # guardar diccionario pickle sin vectorizacion
        pickle.pickleSaveDic(diccionario_notas_sin_vector)

        # Palabras vectorizadas
        WE_vector = wordE.word_embedding_fasttext(diccionario_notas_sin_vector)

        # guardar diccionario pickle con vectorizacion
        pickle.pickleSaveBiomedicalCasedWE(WE_vector)

        # LABORATORIOS ------------------------------------------------------------------------------------------------
        # recoleccion de laboratorios
        conexion_db = sql.openDBconect(
            propiedadesUsuario=["localhost", "root", "MySQLRootPass2021", "enfermedadesrespiratorias"])
        datos_labs_mysql = sql.recolectar_labs(conexion_db)
        sql.closeDBconect(conexion_db)

        # Preprocesar datos de lab
        df_labs = dataOrganize.preprosLabs(datos_labs_mysql)

        # Exportar resultado dataframe a .csv
        expcsv.exportCsvLabs(df_labs, 'LabsPreprocesados')

        answer = None
    elif answer == 2:
        dic_pickle_sin_vector = pickle.pickleCargarDic()
        lista_biomedica_cased_pickle = pickle.pickleLoadBiomedicalCasedWE()

        answer = None
    elif answer == 3:
        dic_pickle_sin_vector = pickle.pickleCargarDic()
        lista_biomedica_cased_pickle = pickle.pickleLoadBiomedicalCasedWE()

        expcsv.exportCsv(lista_biomedica_cased_pickle)

        answer = None
    elif answer == 4:
        # Cargar notas clinicas de pickle
        dic_pickle_sin_vector = pickle.pickleCargarDic()
        lista_biomedica_cased_pickle = pickle.pickleLoadBiomedicalCasedWE()

        # Cargar laboratorios clinicos de .csv
        df_labs = expcsv.importCsvLabs()

        answer = None
    else:
        salir = True
        print('\nAccion Cancelada\nfin del programa'.upper())

        answer = None

    while not salir:

        answer = input(
            "\nFAVOR DE SELECCIONAR UNA OPCION\n\t1-ANALIZAR MODELO WORD EMBEDDING\n\t0-CANCELAR/SALIR\n\tRESPUESTA: ")
        if answer.isdigit():
            try:
                answer = int(answer)
                if answer >= 0 and answer <= 1:
                    break
                else:
                    print("\nError, Favor de seleccionar la opciones disponibles".upper())
            except ValueError:
                print("\nError, Favor de seleccionar la opciones disponibles".upper())
        else:
            print("\nError, Favor de seleccionar la opciones disponibles".upper())


    if answer == 1:
        while True:
            answer2 = input("\nFAVOR DE SELECCIONAR UNA OPCION\n\t"
                            "1-CONFIGURACION DE PARAMETROS GENERAL\n\t"
                            "2-COMPARATIVA TECNICAS EMBEBIDAS\n\t"
                            "3-PRUEBAS FINALES CON BILSTM\n\t"
                            "4-PRUEBAS FINALES CON BILSTM + LABS\n\t"
                            "0-CANCELAR/SALIR\n\tRESPUESTA: ")

            if answer2.isdigit():
                try:
                    answer2 = int(answer2)
                    if answer2 >= 0 and answer2 <= 4:
                        break
                    else:
                        print("\nError, Favor de seleccionar la opciones disponibles".upper())
                except ValueError:
                    print("\nError, Favor de seleccionar la opciones disponibles".upper())
            else:
                print("\nError, Favor de seleccionar la opciones disponibles".upper())

        if answer2 == 1:
            print('FASE 1: Configuración de parámetros, mediante técnica jerárquica.')

            WE = list(lista_biomedica_cased_pickle[0].keys())
            WE_key = WE[0]
            WE_tec = list(lista_biomedica_cased_pickle[0][WE_key].keys())
            # Datos Biomedicos Cbow Cased
            WE_used = WE_tec[8]
            x_y_datos = dataOrganize.organizar_datos_IO(lista_biomedica_cased_pickle[0], WE_used, 10)

            dic_iter_param = {
                'optimizer': ['adam', 'SGD'],
                'learning_rate': [0.01, 0.025, 0.05, 0.1, 0.5],
                'units_memory': [5, 10, 20, 50, 100],
                'dense': [1, 2, 3, 4, 5],
                'epoch': [5, 10, 25, 50, 100]
            }

            dic_param = {
                'optimizer': dic_iter_param['optimizer'][0],
                'learning_rate': dic_iter_param['learning_rate'][0],
                'units_memory': dic_iter_param['units_memory'][0],
                'dense': dic_iter_param['dense'][0],
                'epoch': dic_iter_param['epoch'][0]
            }

            dic_result = {}

            print(
                '\nIniciando Pruebas Iteradas___________________________________________________________________'.upper())
            now_start = datetime.now()
            for nombre_parametro in dic_iter_param:
                key_result = []
                key_result_value = []
                for parametro in dic_iter_param[str(nombre_parametro)]:
                    key_result.append(str(nombre_parametro) + '_' + str(parametro))
                    dic_param[str(nombre_parametro)] = parametro
                    param_iter = str(nombre_parametro) + '_' + str(parametro)
                    print('\n\tInicio Nuevo Modelado'.upper())
                    print('\tParametro iterado \"' + str(nombre_parametro) + '\" : ' + str(parametro))
                    print('\tParametros usados: ' + str(dic_param) + '\n')

                    res_prom_BiLSTM = BILSTMmodel.model_BILSTM(x_y_datos, dic_param, param_iter, 10, False, True)

                    key_result_value.append(res_prom_BiLSTM[1][3])  # VALOR VALIDACION F1

                id_key_result = key_result_value.index(max(key_result_value))
                best_param = dic_iter_param[nombre_parametro][id_key_result]
                dic_param[str(nombre_parametro)] = best_param
                dic_result[str(key_result[id_key_result])] = max(key_result_value)
                print(str(key_result[id_key_result]) + ' = ' + str(max(key_result_value)))

            print('MEJORES PARAMETROS Y RESULTADOS FINALES POR PARAMETRO')
            print(dic_param)
            print(dic_result)
            now_final = datetime.now()
            nombre_param = 'Param_best_WE-' + str(WE_used) + '_txt-'
            nombre_result = 'Param_result_WE-' + str(WE_used) + '_txt-'
            textR.save_best_param(dic_param, nombre_param, WE_used, now_start, now_final)
            textR.save_result_param(dic_result, nombre_result, WE_used, now_start, now_final)

            # Grabar diccionarios resultantes en pickle
            pickle.pickleSaveParamDic(dic_param, WE_used)
            pickle.pickleSaveResultDic(dic_result, WE_used)

        elif answer2 == 2:
            print('FASE 2: COMPARATIVA TECNICAS EMBEBIDAS')
            now_start = datetime.now()

            WE = list(lista_biomedica_cased_pickle[0].keys())
            WE_key = WE[0]
            WE_tec = list(lista_biomedica_cased_pickle[0][WE_key].keys())

            # Datos Biomedicos Cbow Cased
            WE_Name_BioCbowCased = WE_tec[8]
            x_y_datos_BioCbowCased = dataOrganize.organizar_datos_IO(lista_biomedica_cased_pickle[0],
                                                                     WE_Name_BioCbowCased, 33)

            # Datos Biomedicos Skipgram Cased
            WE_Name_BioSkipCased = WE_tec[10]
            x_y_datos_BioSkipCased = dataOrganize.organizar_datos_IO(lista_biomedica_cased_pickle[0],
                                                                     WE_Name_BioSkipCased, 33)

            # Datos Biomedicos Cbow Uncased
            WE_Name_BioCbowUncased = WE_tec[12]
            x_y_datos_BioCbowUncased = dataOrganize.organizar_datos_IO(lista_biomedica_cased_pickle[0],
                                                                       WE_Name_BioCbowUncased, 33)

            # Datos Biomedicos Skipgram Uncased
            WE_Name_BioSkipUncased = WE_tec[14]
            x_y_datos_BioSkipUncased = dataOrganize.organizar_datos_IO(lista_biomedica_cased_pickle[0],
                                                                       WE_Name_BioSkipUncased, 33)

            # Datos CLinicos Cbow Cased
            WE_Name_ClinCbowCased = WE_tec[16]
            x_y_datos_ClinCbowCased = dataOrganize.organizar_datos_IO(lista_biomedica_cased_pickle[0],
                                                                      WE_Name_ClinCbowCased, 33)

            # Datos Clinicos Skipgram Cased
            WE_Name_ClinSkipCased = WE_tec[18]
            x_y_datos_ClinSkipCased = dataOrganize.organizar_datos_IO(lista_biomedica_cased_pickle[0],
                                                                      WE_Name_ClinSkipCased, 33)

            Periodo = 1
            Graficas = True
            aleatoridad = False
            DataValidation = False

            dic_param_propios_3 = {
                'optimizer': 'SGD',
                'learning_rate': 0.1,
                'units_memory': 50,
                'dense': 1,
                'epoch': 100
            }

            # Texto Biomedico con vectorizado con FastText Biomedico Cbow Cased.
            nameConf = 'Conf3_' + str(WE_Name_BioCbowCased)
            res_prop3_BioCbowCased = BILSTMmodel.model_BILSTM(x_y_datos_BioCbowCased, dic_param_propios_3, nameConf,
                                                              Periodo, Graficas, aleatoridad, DataValidation)

            # Texto Biomedico con vectorizado con FastText Biomedico Skipgram Cased.
            nameConf = 'Conf3_' + str(WE_Name_BioSkipCased)
            res_prop3_BioSkipCased = BILSTMmodel.model_BILSTM(x_y_datos_BioSkipCased, dic_param_propios_3, nameConf,
                                                              Periodo, Graficas, aleatoridad, DataValidation)

            # Texto Biomedico con vectorizado con FastText Biomedico Cbow Uncased.
            nameConf = 'Conf3_' + str(WE_Name_BioCbowUncased)
            res_prop3_BioCbowUncased = BILSTMmodel.model_BILSTM(x_y_datos_BioCbowUncased, dic_param_propios_3, nameConf,
                                                                Periodo, Graficas, aleatoridad, DataValidation)

            # Texto Biomedico con vectorizado con FastText Biomedico Skipgram Uncased.
            nameConf = 'Conf3_' + str(WE_Name_BioSkipUncased)
            res_prop3_BioSkipUncased = BILSTMmodel.model_BILSTM(x_y_datos_BioSkipUncased, dic_param_propios_3, nameConf,
                                                                Periodo, Graficas, aleatoridad, DataValidation)

            # Texto Biomedico con vectorizado con FastText Clinico Cbow Cased.
            nameConf = 'Conf3_' + str(WE_Name_ClinCbowCased)
            res_prop3_ClinCbowCased = BILSTMmodel.model_BILSTM(x_y_datos_ClinCbowCased, dic_param_propios_3, nameConf,
                                                               Periodo, Graficas, aleatoridad, DataValidation)

            # Texto Biomedico con vectorizado con FastText Clinico Skipgram Cased.
            nameConf = 'Conf3_' + str(WE_Name_ClinSkipCased)
            res_prop3_ClinSkipCased = BILSTMmodel.model_BILSTM(x_y_datos_ClinSkipCased, dic_param_propios_3, nameConf,
                                                               Periodo, Graficas, aleatoridad, DataValidation)

            now_final = datetime.now()

        elif answer2 == 3:
            now_start = datetime.now()
            print('INICIO PRUEBAS FINALES CON BILSTM\n\tTiempo Inicio: ' + str(now_start))

            WE = list(lista_biomedica_cased_pickle[0].keys())
            WE_key = WE[0]
            WE_tec = list(lista_biomedica_cased_pickle[0][WE_key].keys())
            # Datos Biomedicos Cbow Cased
            WE_used = WE_tec[10]
            group_data = dataOrganize.OrganizeGroupData_IO(lista_biomedica_cased_pickle[0], WE_used, 33)

            # group_data 1:Control vs enfermedades
            # group_data 2:Embolia vs otros
            # group_data 3:Neumonia vs otros
            # group_data 4,5 y 6: Control vs Embolia; Control vs Neumonia; Embolia vs Neumonia

            Periodo = 2  # 20
            Graficas = False
            aleatoridad = True
            DataValidation = True

            dic_param = {
                'optimizer': 'SGD',
                'learning_rate': 0.1,
                'momentum': 0.1,
                'units_memory': 50,
                'dense': 1,
                'epoch': 25
            }

            for i in range(1, len(group_data)):
                t_start = datetime.now()
                t_now = t_start.strftime("%d.%m.%Y %H-%M-%S")
                nameConf = 'Grupo-' + str(i) + '_' + str(t_now)
                print('\t\n' + str(nameConf))

                pruebaC_Enf = BILSTMmodel.model_BILSTM(group_data[i], dic_param, nameConf, Periodo, Graficas,
                                                       aleatoridad, DataValidation)
                t_final = datetime.now()

            now_final = datetime.now()
            print('FIN PRUEBAS FINALES \n\tTiempo Final: ' + str(now_final))

        elif answer2 == 4:
            now_start = datetime.now()
            print('INICIO PRUEBAS FINALES CON BILSTM + LABS\n\tTiempo Inicio: ' + str(now_start))

            WE = list(lista_biomedica_cased_pickle[0].keys())
            WE_key = WE[0]
            WE_tec = list(lista_biomedica_cased_pickle[0][WE_key].keys())
            WE_used = WE_tec[10]
            group_data = dataOrganize.joinWELabs_IO(lista_biomedica_cased_pickle[0], df_labs.copy(), WE_used, 33)

            # group_data 1:Control vs enfermedades
            # group_data 2:Embolia vs otros
            # group_data 3:Neumonia vs otros
            # group_data 4,5 y 6: Control vs Embolia; Control vs Neumonia; Embolia vs Neumonia

            Periodo = 20  # 20
            Graficas = False
            aleatoridad = True
            DataValidation = True

            dic_param = {
                'optimizer': 'SGD',
                'learning_rate': 0.1,
                'momentum': 0.1,
                'units_memory': 50,
                'dense': 1,
                'epoch': 25
            }

            for i in range(1, len(group_data)):
                t_start = datetime.now()
                t_now = t_start.strftime("%d.%m.%Y %H-%M-%S")
                nameConf = 'Grupo-' + str(i) + '_' + str(t_now)
                print('\t\n' + str(nameConf))

                pruebaC_Enf = BILSTMmodel.model_BILSTM(group_data[i], dic_param, nameConf, Periodo, Graficas,
                                                       aleatoridad, DataValidation)
                t_final = datetime.now()

            now_final = datetime.now()
            print('FIN PRUEBAS FINALES MAS LABS \n\tTiempo Final: ' + str(now_final))

        else:
            print('\nAccion Cancelada\nfin del programa'.upper())

    else:
        print('\nAccion Cancelada\nfin del programa'.upper())

    return None


main()

