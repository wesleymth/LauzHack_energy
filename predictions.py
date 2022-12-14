from dataset_generator import *
from joblib import dump, load
from data_processing import rename_categorical_cols
from train_model import one_hot_encoding

def predict(df):
    model = load('linear.joblib')
    return model.predict(df)

def energy(model, X):
    dall = {}
    for d in [get_cpu_features(), get_system_features()]:
        dall.update(d)
    dataset = pd.DataFrame([],columns=list(dall.keys()) + ["model_name", "nb_samples", "nb_preds"])
    
    dataset.loc[len(dataset)] = list(dall.values()) + [model.__name__, X.shape[0], X.shape[1]]
    dataset = rename_categorical_cols(dataset)
    onehot = load('one_hot_encoder.joblib')
    transformed = onehot.transform(dataset)
    one_hot_df = pd.DataFrame(transformed.todense(), columns=onehot.get_feature_names_out())
    return predict(one_hot_df)
