import graphviz
import Funciones.textFile as textfile

def exportResult(modelResult,nameFile):

    indexModel=modelResult[0]
    dot_graph=modelResult[1]
    accuracy=modelResult[2]
    precision=modelResult[3]
    recall=modelResult[4]
    specificity=modelResult[5]
    f1score=modelResult[6]
    f1average=modelResult[7]

    graph = graphviz.Source(dot_graph, format="png")
    graph
    graph.render('DT_F1_'+str(nameFile))

    texto= ('Valor F1 Promedio:'+str(f1average)+
            '\nIteracion del Modelo Correspondiente:'+str(indexModel+1)+
            '\nF1 resultante:'+str(f1score)+
            '\nExactitud resultante: ' + str(accuracy)+
            '\nPrecision resultante: ' + str(precision)+
            '\nRecall resultante: ' + str(recall)+
            '\nEspecificidad resultante: ' + str(specificity))

    nameText='F1_result_'+str(nameFile)
    textfile.text_file(texto,nameText)

    print('\nF1 promedio: '+str(f1average)+'\nF1 cercano: '+str(f1score)+'\nEspecificidad: '+str(specificity))

    return None