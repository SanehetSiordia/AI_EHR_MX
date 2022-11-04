from sklearn.preprocessing import LabelEncoder
import pandas as pd

def pre_data(data):
    result=None
    df = data

    inputs = df.drop('diagnostico_final', axis='columns')
    target = df['diagnostico_final']

    target_names = pd.unique(target).tolist()
    inputs_names = list(inputs.columns)

    target_label = LabelEncoder()
    target = target_label.fit_transform(target)
    inputs_arrays = inputs.to_numpy()
    x = inputs_arrays
    y = target

    result=[x,y,target_names,inputs_names]
    return(result)