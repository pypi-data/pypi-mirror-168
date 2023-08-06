# Importing the Packages:
import optuna
import mlflow
import os

# try:
#     from sklearn.utils import safe_indexing
# except ImportError:
#     from sklearn.utils import _safe_indexing

from pathlib import Path
from pycaret.classification import *
from sklearn.metrics import recall_score
from mlflow.models.signature import infer_signature
from explainerdashboard import ExplainerDashboard, ClassifierExplainer

SENSORS_FEATURES = [
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

STAGES = ["baseline", "absorb", "pause", "desorb", "flush"]
TARGET_COL = "result"
# REMOTE_TRACKING_URI = "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"
REMOTE_TRACKING_URI = "http://ec2-18-133-140-90.eu-west-2.compute.amazonaws.com:5000/"



# 'http://ec2-3-10-210-150.eu-west-2.compute.amazonaws.com:5000/'


def get_plots(model):
    """_summary_

    Args:
        model (_type_): _description_
    """

    model_attributes = dir(model)

    plot_dir = os.path.join(os.getcwd(), "plots")
    Path(plot_dir).mkdir(parents=True, exist_ok=True)

    plot_model(model, plot="confusion_matrix", save=plot_dir)
    cm = os.path.join(plot_dir, "Confusion Matrix.png")
    # mlflow.log_artifact(cm)
    # log_artifact(cm)

    plot_model(model, plot="class_report", save=plot_dir)
    cr = os.path.join(plot_dir, "Class Report.png")
    # mlflow.log_artifact(cr)
    # log_artifact(cr)

    if "predict_proba" in model_attributes:
        try:
            plot_model(model, plot="auc", save=plot_dir)
            auc = os.path.join(plot_dir, "AUC.png")
            # mlflow.log_artifact(auc)

            plot_model(model, plot="pr", save=plot_dir)
            pr = os.path.join(plot_dir, "Precision Recall.png")
            # mlflow.log_artifact(pr)

            plot_model(model, plot="calibration", save=plot_dir)
            cc = os.path.join(plot_dir, "Calibration Curve.png")
            # mlflow.log_artifact(cc)
        except:
            pass

    if "feature_importances_" in model_attributes:
        plot_model(model, plot="feature", save=plot_dir)
        fi = os.path.join(plot_dir, "Feature Importance.png")
        # mlflow.log_artifact(fi)

    mlflow.log_artifact(plot_dir)


def specificity(actual, pred, pos_label=0):
    """_summary_

    Args:
        actual (_type_): _description_
        pred (_type_): _description_
        pos_label (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    return recall_score(actual, pred, pos_label=pos_label)


def objective(trial, df, study_name, model_mode):
    """_summary_

    Args:
        trial (_type_): _description_
        df (_type_): _description_
        study_name (_type_): _description_
        model_mode (_type_): _description_
    """



    mlflow.set_experiment(study_name)

    mlflow.set_tracking_uri(REMOTE_TRACKING_URI)


    df_offset = df.filter(regex='offset')
    df_gradient = df.filter(regex='gradient')

    if len(df_offset.columns) > 0:
        offset = True
    else:
        offset = False

    if len(df_gradient.columns) > 0:
        gradient = True
    else:
        gradient = False
    

    df_copy = df.copy(deep=True)

    relevant_features = list(df_copy.drop(TARGET_COL, axis=1).columns)

    mlflow.start_run()

    # remove unwanted characters from the column names
    df_copy.columns = df_copy.columns.str.replace('["]', "")

    features = df_copy.drop(TARGET_COL, axis=1)
    # map_dict = {"Control": 0, "Covid": 1}
    # df_copy["result"] = df_copy["result"].replace(map_dict)

    clf = setup(
        df_copy,
        target=TARGET_COL,
        silent=True,
        log_plots=True,
        experiment_name=study_name,
        preprocess=False,
        remove_multicollinearity=True,
        multicollinearity_threshold=1.0,
        fold=5
    )

    exp_description = pull()
    map_dict = dict(exp_description.data[exp_description.data['Description'] == 'Label Encoded']['Value'])

    add_metric("specificity", "Specificity", specificity)
    remove_metric("MCC")
    remove_metric("Kappa")

    MODELS = dict(models()["Name"])

    if model_mode == "random":

        model_id = trial.suggest_categorical("model", list(MODELS.keys()))
        model_name = MODELS[model_id]
        model = create_model(model_id)
        predict_model(model)
        metrics = pull().iloc[:, 1:]
        keys = metrics.columns
        values = metrics.values[0]
        metrics = dict(zip(keys, values))

        # get_plots(model)

        conda_env = mlflow.pyfunc.get_default_conda_env()
        conda_env['dependencies'].append({'pip': [
            'pickle5'
            'scikit-learn==0.23.2'
            #... some other dependencies
            ]})

        signature = infer_signature(features, predict_model(model, data=features))
        mlflow.sklearn.log_model(model, artifact_path=model_name, signature=signature, conda_env=conda_env)

    # elif model_mode == 'xgb':

    #     model = create_model('xgb')
    #     predict_model(model)
    #     metrics = pull().iloc[:,1:]
    #     keys = metrics.columns
    #     values = metrics.values[0]
    #     metrics = dict(zip(keys, values))

    #     get_plots(model)
    #     mlflow.sklearn.log_model(model, artifact_path=model_name)

    else:

        model = compare_models()

        model_name = model.__class__.__name__
        predict_model(model)
        metrics = pull().iloc[:, 1:]
        keys = metrics.columns
        values = metrics.values[0]
        metrics = dict(zip(keys, values))

        get_plots(model)

        signature = infer_signature(features, predict_model(model, data=features))
        mlflow.sklearn.log_model(model, artifact_path=model_name, signature=signature)

    model_params = model.get_params()





    data_dir = os.path.join(os.getcwd(), "data")
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    X_train = get_config('X_train')
    y_train = get_config('y_train')
    X_test = get_config('X_test')
    y_test = get_config('y_test')

    df_test = X_test.join(y_test)
    df_train = X_train.join(y_train)

    df_train.to_csv(os.path.join(data_dir, 'train.csv'))
    df_test.to_csv(os.path.join(data_dir, 'test.csv'))
    
    mlflow.log_artifact(data_dir)


    dashboard_dir = os.path.join(os.getcwd(), "dashboard")
    Path(dashboard_dir).mkdir(parents=True, exist_ok=True)

    try:
        explainer = ClassifierExplainer(model, X_test, y_test)
        db = ExplainerDashboard(explainer, 
                            # defaults to "Model Explainer"
                            whatif=False,
                            shap_interaction=False
                            )

        db.save_html(os.path.join(dashboard_dir, 'dash.html'))

        mlflow.log_artifact(dashboard_dir)
    except:
        pass
    

    




    mlflow.log_metrics(metrics)

    try:
        # mlflow.set_tag('features', features)
        mlflow.set_tag("relevant_features", relevant_features)

    except:
        pass

    mlflow.set_tag("model_name", model_name)
    mlflow.set_tag("offset", offset)
    mlflow.set_tag("gradient", gradient)
    mlflow.set_tag("model_params", model_params)
    mlflow.set_tag("map_dict", map_dict)


    mlflow.set_tag("model_mode", model_mode)

    mlflow.end_run()


def train_experiments(
    df, study_name="supervised", direction="maximize", model_mode="random", n_trials=5
):
    """trains several models during different trials and logs them. Experiemnt can be tracked on "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"


    Args:
        df (pandas dataframe): dataframe of cyclic sensor data to be used for training
        study_name (str, optional): optuna study name to use. Defaults to 'raptor'.
        direction (str, optional): direction of objective. Defaults to 'maximize'.
        model_mode (str, optional): _description_. Defaults to 'random'.
        n_trials (int, optional): number of times to run experiments. Defaults to 5.
    """

    study = optuna.create_study(study_name=study_name, direction=direction)
    study.optimize(
        lambda trial: objective(trial, df, study_name, model_mode), n_trials=n_trials
    )

    print("Click on this link to track experiments: ", REMOTE_TRACKING_URI)
