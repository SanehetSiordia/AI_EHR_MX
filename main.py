import os
#Exportar Funciones de Apoyo
import Funciones.dataRead as dataRead
import Funciones.dataPreparation as dataPre
import Funciones.modelDT as modelDT
import Funciones.pickleSave as pickleSave
import Funciones.compareModels as compareDT
import Funciones.exportResults as exportResult


def main():
    print('Inicio del programa--------------------'.upper())
    #Cargar archivo________________________________________
    #nameFile = 'Data_E-C'
    nameFile = 'Data_E-N'
    #nameFile = 'Data_N-C'
    #nameFile = 'Data_C-Enf'
    #nameFile = 'Data_E-Otros'
    #nameFile = 'Data_N-Otros'

    ciclos=100
    diccModels={}

    linkFile = os.path.abspath(os.getcwd())+'\Data\\'+nameFile
    data = dataRead.data_read(linkFile)

    if data[0]:
    #Preparar Datos________________________________________
        print("\n\t Inicio del preprocesado de datos".upper())
        predata=dataPre.pre_data(data[1])
        print("\n\t Fin del preprocesado de datos".upper())

    #Modelar Datos_________________________________________
        print("\n\tinicio de ciclos de modelados".upper())
        for i in range(ciclos):
            modeldata=modelDT.model_dt(predata)
            diccModels[str(nameFile)+'_ciclo_'+str(i)] = modeldata
        print("\n\tfin de ciclos de modelados".upper())

    #exportar dict a plickle
        print("\n\tinicio de exportacion a pickle".upper())
        pickleSave.pickleExport(diccModels,nameFile)
        print("\n\tfin de exportacion a pickle".upper())

    #Comparar resultados
        print("\n\tInicio de la Comparacion de resultados".upper())
        bestModel=compareDT.compareModelsDT(diccModels)
        print("\n\tFin de la Comparacion de resultados".upper())

    #Exportar resultados
        print("\n\tInicio de la exportacion de resultados".upper())
        exportResult.exportResult(bestModel,nameFile)
        print("\n\tFin de la exportacion de resultados".upper())

    else:
        print('No hay datos cargados')
    print('\nFin del programa--------------------'.upper())
    return None
main()
