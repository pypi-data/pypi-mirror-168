import argparse
import configparser
import logging
import os

import mlflow
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import mean_squared_error

from housing import mlflow_utils, setup_logger

logger = logging.getLogger(__file__)


def load_validating_data(data_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load validation data from <data_path>/processed/val_housing.csv

    Parameters
    ----------
    data_path : str
        directory where dataset was downloaded

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        X_val, y_val dataframes
    """
    val_data_path = os.path.join(data_path, "processed", "val_housing.csv")
    data = pd.read_csv(val_data_path, index_col=0)
    X_val = data.drop("median_house_value", axis=1)
    y_val = data["median_house_value"].copy()
    logger.info(f"Validation data with shape {X_val.shape} loaded")
    return X_val, y_val


def load_mlflow_models() -> list[mlflow.entities.model_registry.RegisteredModel]:
    """returns all the registered models in mlflow

    Returns
    -------
    list[mlflow.entities.model_registry.RegisteredModel]
        list of registered models in mlflow
    """
    client = mlflow.tracking.MlflowClient()
    reg_models = client.list_registered_models()
    logger.info(f"Found {len(reg_models)} registered models")
    return reg_models


def score_model(
    model: sklearn.base.BaseEstimator, model_desc: str, X: pd.DataFrame, y: pd.DataFrame
):
    """Prints MSE (mean squared error) and RMSE (root mean squared error) of the model

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        trained sklearn model
    model_desc : str
        name of the model
    X : pd.DataFrame
        X_val for validation
    y : pd.DataFrame
        y_val for validation
    """
    final_predictions = model.predict(X)
    final_mse = mean_squared_error(y, final_predictions)
    final_rmse = np.sqrt(final_mse)
    logger.info("{} RMSE: {}".format(model_desc, final_rmse))
    return (final_mse, final_rmse)


def update_model_metrics(run_id: str, mse: float, rmse: float):
    """Update metrics of previous run with validation metrics

    Parameters
    ----------
    run_id : str
        id of past run which is to be updated
    mse : float
        validation mean square error metric
    rmse : float
        validation root mean square error metric
    """
    with mlflow.start_run(run_id=run_id):
        mlflow.log_metric("val_mse", mse)
        mlflow.log_metric("val_rmse", rmse)


@mlflow_utils.mlflow_conf
def main(**kwargs):
    """main funciton of score.py"""
    if kwargs.get("console_log"):
        setup_logger.add_log_handler(logger, logging.StreamHandler())
    if kwargs.get("log_path"):
        log_file = __file__.split("/")[-1] + ".log"
        complete_path = os.path.join(kwargs.get("log_path"), log_file)
        os.makedirs(os.path.dirname(complete_path), exist_ok=True)
        setup_logger.add_log_handler(logger, logging.FileHandler(complete_path))
    setup_logger.set_log_level(logger, kwargs.get("log_level"))

    X_test, y_test = load_validating_data(kwargs.get("data_path"))

    reg_models = load_mlflow_models()
    for reg_model in reg_models:
        model_uri = f"models:/{reg_model.name}/1"
        loaded_model = mlflow.sklearn.load_model(model_uri)
        final_mse, final_rmse = score_model(
            loaded_model, reg_model.name, X_test, y_test
        )
        update_model_metrics(
            reg_model.latest_versions[-1].run_id, final_mse, final_rmse
        )


def generate_argument_parser() -> argparse.ArgumentParser:
    """Returns argument parser for the script housing.score

    Returns
    -------
    argparse.ArgumentParser
        argument parser with required arguments added
    """
    parser = argparse.ArgumentParser(
        description="This script use trained models to find their performance on \
            validation datasets"
    )
    parser.add_argument(
        "-d", "--data_path", type=str, help="Path for the data folder (raw & processed)"
    )
    parser.add_argument(
        "-a", "--artifacts_path", type=str, help="Path for the artifacts folder"
    )
    parser.add_argument(
        "--console-log",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Whether to print log to console of not (True/False)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        help="Specify log level (critical, error, warn, warning, info, debug) \
            Default: debug",
    )
    parser.add_argument(
        "--log-path",
        type=str,
        help="Specify path where log files should be generated",
    )
    return parser


if __name__ == "__main__":
    config = configparser.ConfigParser()
    main_base = os.path.dirname(__file__)
    config_file = os.path.join(main_base, "housing.cfg")
    config.read(config_file)
    defaults = config["defaults"]
    params = dict(defaults)
    params["console_log"] = config.getboolean("defaults", "console_log")

    parser = generate_argument_parser()
    args = vars(parser.parse_args())
    params.update({k: v for k, v in args.items() if v is not None})

    main(**params)
