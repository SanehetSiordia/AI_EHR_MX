##  **Decision Tree Analysis Branch**

This section is part of the study for the article “Pneumonia and Pulmonary Thromboembolism Classification Using Electronic Health Records” DOI: [_**10.3390/diagnostics12102536**_](https://doi.org/10.3390/diagnostics12102536). 

The .csv files created in the SQLtoCSV section and saved in the path: *\AI_EHR_MX\Data* were modified to use only structured data without sensitive information and were suitable for a binary type of classification 1 vs 1 and 1 vs all.

The Sklearn package was used to generate and evaluate the model of the Decision Tree, and the *Graphviz v0.20.1* package was used to graph the models.

The results of the graphs are saved in .png type files in the root of the project and the metrics result are saved in .txt files in the path *\AI_EHR_MX\Txt_Result*.

The **code** with the specifications, sampling and evaluation metrics of the model is shown below:

``` py
skf= StratifiedKFold(n_splits=5, shuffle=True, random_state=2) 

tree_clf = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=3, min_samples_split=5)

for train_index, test_index in skf.split(x, y):
    i += 1
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    model = tree_clf.fit(x_train, y_train)

    acu = accuracy_score(y_test, y_predict)
    pre = precision_score(y_test, y_predict, average='macro')
    rec = recall_score(y_test, y_predict, average='macro')
    f1 = f1_score(y_test, y_predict, average='macro')
```

**Author's note**
>The original .csv files used for the project are shared in the path *\AI_EHR_MX\Data*. 












