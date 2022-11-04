from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.tree import export_graphviz

def model_dt(predata):
    result=None
    #Listas para resultados
    list_dot=[]
    list_acu_result=[]
    list_pre_result=[]
    list_rec_result=[]
    list_f1_result=[]
    list_spe_result=[]

    x=predata[0]
    y=predata[1]
    target_names=predata[2]
    inputs_names=predata[3]

    instances=len(y)

    #variables de evaluacion
    i = 0
    acu_Result=0.0
    pre_Result=0.0
    rec_Result=0.0
    f1_Result=0.0
    #cm_Result=None
    #cm_Result_Exist=False

    spe_Result=0.0

    #Muestreo KFOLD
    #kf = KFold(n_splits=5, shuffle=True, random_state=2)               #K HOLD sin estratificar

    skf= StratifiedKFold(n_splits=5, shuffle=True, random_state=2)      #K HOLD estratificado

    #Iniciador del modelo DT
    tree_clf = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=3, min_samples_split=5)

    #Iteracion de entrenamiento K veces
    #or train_index, test_index in kf.split(x):         #K HOLD sin estratificar

    for train_index, test_index in skf.split(x, y):     #K HOLD estratificado
        i += 1
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]

        #Contruccion del modelo y data para graficar DT
        #con datos de entrenamiento
        model = tree_clf.fit(x_train, y_train)
        dot_data = export_graphviz(tree_clf, out_file=None,
                                   feature_names=inputs_names,
                                   class_names=target_names,
                                   filled=True, rounded=True,
                                   special_characters=True)
        list_dot.append(dot_data)

        #Prediccion del Modelo
        y_predict = model.predict(x_test)

        #Evaluacion del modelo
        acu = accuracy_score(y_test, y_predict)
        pre = precision_score(y_test, y_predict, average='macro')
        rec = recall_score(y_test, y_predict, average='macro')
        f1 = f1_score(y_test, y_predict, average='macro')
        #cm = confusion_matrix(y_test, y_predict)
        tn, fp, fn, tp = confusion_matrix(y_test, y_predict).ravel()
        specificity = tn / (tn + fp)

        list_acu_result.append(acu)
        list_pre_result.append(pre)
        list_rec_result.append(rec)
        list_f1_result .append(f1)
        list_spe_result.append(specificity)

        #Evaluacion Promedio del Modelo
        acu_Result = acu_Result + acu
        pre_Result = pre_Result + pre
        rec_Result = rec_Result + rec
        f1_Result = f1_Result + f1
        #if cm_Result is None:
        #    cm_Result = cm
        #if cm_Result_Exist is True:
        #    for j in range(len(cm)):
        #        for k in range(len(cm[j])):
        #            cm_Result[j][k] = cm_Result[j][k] + cm[j][k]
        #cm_Result_Exist = True

        spe_Result = spe_Result + specificity

    # RESULTADOS PROMEDIOS DE TODAS LAS ITERACIONES
    acu_Result = round(acu_Result / i, 3)
    pre_Result = round(pre_Result / i, 3)
    rec_Result = round(rec_Result / i, 3)
    f1_Result = round(f1_Result / i, 3)

    #for j in range(len(cm_Result)):
    #    for k in range(len(cm_Result[j])):
    #        if cm_Result[j][k] > 0:
    #            cm_Result[j][k] = round(cm_Result[j][k] / i)

    spe_Result = round(spe_Result / i, 3)

    #COMPARATIVA DE RESULTADOS AL MAS CERCANO AL F1 Promedio
    closest=min(list_f1_result, key=lambda x:abs(x-f1_Result))
    idx=list_f1_result.index(closest)

    result=[idx,list_dot[idx],list_acu_result[idx],list_pre_result[idx],list_rec_result[idx],list_spe_result[idx],list_f1_result[idx],f1_Result]
    return result





