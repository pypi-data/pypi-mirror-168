import numpy as np
import pandas as pd
import xgboost as xgb
from boruta import BorutaPy
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import (
    ComprehensiveFCParameters,
    extract_features,
)
from tsfresh import extract_features
from .preprocess import offset_batch_samples, gradient_batch_samples


FEATURES = [
    "sensor_1",
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_5",
    "sensor_6",
    "sensor_7",
    "sensor_8",
    "sensor_9",
    "sensor_10",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_14",
    "sensor_15",
    "sensor_16",
    "sensor_17",
    "sensor_18",
    "sensor_19",
    "sensor_20",
    "sensor_21",
    "sensor_22",
    "sensor_23",
    "sensor_24",
]

# TARGET_COL = "result"

extraction_settings = ComprehensiveFCParameters()


def get_all_features(
    X,
    features,
    unique_id="exp_unique_id",
    timesteps="timesteps"
):
    """_summary_

    Args:
        X (_type_): _description_
        features (_type_): _description_
        unique_id (str, optional): _description_. Defaults to "exp_unique_id".
        timesteps (str, optional): _description_. Defaults to "timesteps".

    Returns:
        _type_: _description_
    """

    # features = [col for col in X if col.startswith('sensor')]
    features = [unique_id, timesteps] + features

    X = X[features]

    # X = df.drop(label, axis=1)
    # y = df.groupby(unique_id).first()[label]

    

    X_extracted = extract_features(
        X,
        column_id=unique_id,
        column_sort=timesteps,
        default_fc_parameters=extraction_settings,
        # we impute = remove all NaN features automatically
        impute_function=impute,
    )

    return X_extracted


xgb = xgb.XGBClassifier()



def select_relevant_features(X, y, tree_model=xgb):
    """_summary_

    Args:
        X (_type_): _description_
        y (_type_): _description_
        tree_model (_type_, optional): _description_. Defaults to xgb.

    Returns:
        _type_: _description_
    """

    boruta = BorutaPy(
            estimator=tree_model,
            n_estimators="auto",
            max_iter=50,  # number of trials to perform
            perc=100,
            alpha=0.05,
            two_step=False
        )

    # fit Boruta (it accepts np.array, not pd.DataFrame)
    boruta.fit(np.array(X), np.array(y))

    # green and blue area are the important features identified by boruta algorithm
    green_area = X.columns[boruta.support_].to_list()
    blue_area = X.columns[boruta.support_weak_].to_list()

    relevant_features = green_area + blue_area
    X = X[relevant_features]

    return  X


def add_offset_gradient(X_raw, offset=False, gradient=False):
    """_summary_

    Args:
        X (_type_): _description_
        offset (_type_): _description_
        gradient (_type_, optional): _description_. Defaults to xgb.

    Returns:
        _type_: _description_
    """

    
    X_all = []
    X_all.append(X_raw)

    offset, gradient = False, False

    if offset:
        X_offset = offset_batch_samples(X_raw)
        X_offset = X_offset.add_suffix(f'_offset')
        X_all.append(X_offset)

    if gradient:
        X_gradient = gradient_batch_samples(X_raw)
        X_gradient = X_gradient.add_suffix(f'_gradient')
        X_all.append(X_gradient)

    

    X_all = pd.concat(X_all, axis=1)

    return X_all

def get_training_features(df, offset=False, gradient=False, tree_model=xgb, unique_id="exp_unique_id", timesteps="timesteps", label="result", features=FEATURES):
    """_summary_

    Args:
        df (_type_): _description_
        offset (_type_): _description_
        gradient (_type_, optional): _description_. Defaults to xgb.
        tree_model (_type_, optional): _description_. Defaults to xgb.
        unique_id (_type_, optional): _description_. Defaults to
        timesteps (_type_, optional): _description_. Defaults
        label (_type_, optional): _description_. Defaults to
        features (_type_, optional): _description_. Defaults to

    Returns:
        _type_: _description_
    """

    y = df.groupby(unique_id).first()[label]
    X = df.drop(label, axis=1)

    X = add_offset_gradient(X, offset, gradient)

    print('Extracting all features')
    X = get_all_features(X, features=features, unique_id=unique_id, timesteps=timesteps)
    
    print('Selecting relevant features')
    X = select_relevant_features(X, y, tree_model=tree_model)

    df = X.join(y)

    return df

