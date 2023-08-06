import argparse
import configparser
import logging
import os
import pickle

import mlflow
import numpy as np
import pandas as pd
import sklearn
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeRegressor

from housing import mlflow_utils, setup_logger

logger = logging.getLogger(__file__)


def load_training_data(data_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load training data from <data_path>/processed/train_housing.csv

    Parameters
    ----------
    data_path : str
        directory where dataset was downloaded

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        X_train, y_train dataframes
    """
    train_data_path = os.path.join(data_path, "processed", "train_housing.csv")
    data = pd.read_csv(train_data_path, index_col=0)
    X_train = data.drop("median_house_value", axis=1)
    y_train = data["median_house_value"].copy()
    logger.info(f"Training data with shape {X_train.shape} loaded")
    return X_train, y_train


@mlflow_utils.mlflow_conf
@mlflow_utils.mlflow_start_run
def train_linear_reg(X: pd.DataFrame, y: pd.DataFrame) -> sklearn.base.BaseEstimator:
    """Returns a linear regression model trained on passed X, y

    Parameters
    ----------
    X : pd.DataFrame
        X_train for training
    y : pd.DataFrame
        y_train for training

    Returns
    -------
    sklearn.base.BaseEstimator
        trained linear regression model
    """
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    housing_predictions = lin_reg.predict(X)
    lin_mse = mean_squared_error(y, housing_predictions)
    lin_rmse = np.sqrt(lin_mse)
    logger.info(f"Linear regression model trained\n MSE : {lin_mse}\n RMSE: {lin_rmse}")

    mlflow.log_metric("tr_mse", lin_mse)
    mlflow.log_metric("tr_rmse", lin_rmse)
    mlflow.sklearn.log_model(lin_reg, "model", registered_model_name="LinearRegression")

    return lin_reg


@mlflow_utils.mlflow_conf
@mlflow_utils.mlflow_start_run
def train_decision_tree(X: pd.DataFrame, y: pd.DataFrame) -> sklearn.base.BaseEstimator:
    """Returns a decision tree regressor model trained on passed X, y

    Parameters
    ----------
    X : pd.DataFrame
        X_train for training
    y : pd.DataFrame
        y_train for training

    Returns
    -------
    sklearn.base.BaseEstimator
        trained decision tree regressor model
    """
    tree_reg = DecisionTreeRegressor(random_state=42)
    tree_reg.fit(X, y)
    housing_predictions = tree_reg.predict(X)
    tree_mse = mean_squared_error(y, housing_predictions)
    tree_rmse = np.sqrt(tree_mse)
    logger.info(f"Decision tree model trained\n MSE : {tree_mse}\n RMSE: {tree_rmse}")

    mlflow.log_metric("tr_mse", tree_mse)
    mlflow.log_metric("tr_rmse", tree_rmse)
    mlflow.sklearn.log_model(tree_reg, "model", registered_model_name="DecisionTree")

    return tree_reg


@mlflow_utils.mlflow_conf
@mlflow_utils.mlflow_start_run
def train_forest_random_search(
    X: pd.DataFrame, y: pd.DataFrame
) -> sklearn.base.BaseEstimator:
    """Returns a random forest regressor model trained on passed X, y.
    RandomSearchCV isused to search best hyper-parameters for random forest

    Parameters
    ----------
    X : pd.DataFrame
        X_train for training
    y : pd.DataFrame
        y_train for training

    Returns
    -------
    sklearn.base.BaseEstimator
        trained random forest regressor model
    """
    param_distribs = {
        "n_estimators": randint(low=1, high=200),
        "max_features": randint(low=1, high=8),
    }

    forest_reg = RandomForestRegressor(random_state=42)
    rnd_search = RandomizedSearchCV(
        forest_reg,
        param_distributions=param_distribs,
        n_iter=10,
        cv=5,
        scoring="neg_mean_squared_error",
        random_state=42,
    )
    logger.info("Running random search on random forest...")
    rnd_search.fit(X, y)
    cvres = rnd_search.cv_results_
    logger.info("Random search complete, result: ")

    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        logger.info(f"{params}, Mean Score: {-mean_score}")

    # feature_importances = rnd_search.best_estimator_.feature_importances_
    # sorted(zip(feature_importances, X.columns), reverse=True)
    params_str = []
    for key, value in rnd_search.best_params_.items():
        params_str.append(f"{key}-{value}")
    model_name = "forest-" + "-".join(params_str)

    housing_predictions = rnd_search.best_estimator_.predict(X)
    forest_mse = mean_squared_error(y, housing_predictions)
    forest_rmse = np.sqrt(forest_mse)
    logger.info(
        f"Random forest model trained\n MSE : {forest_mse}\n RMSE: {forest_rmse}"
    )

    mlflow.log_params(rnd_search.best_params_)
    mlflow.log_metric("tr_mse", forest_mse)
    mlflow.log_metric("tr_rmse", forest_rmse)
    mlflow.sklearn.log_model(
        rnd_search.best_estimator_, "model", registered_model_name=model_name
    )

    return rnd_search.best_estimator_, model_name


@mlflow_utils.mlflow_conf
@mlflow_utils.mlflow_start_run
def train_forest_grid_search(
    X: pd.DataFrame, y: pd.DataFrame
) -> sklearn.base.BaseEstimator:
    """Returns a random forest regressor model trained on passed X, y.
    GridSearchCV isused to search best hyper-parameters for random forest

    Parameters
    ----------
    X : pd.DataFrame
        X_train for training
    y : pd.DataFrame
        y_train for training

    Returns
    -------
    sklearn.base.BaseEstimator
        trained random forest regressor model
    """
    param_grid = [
        # try 12 (3×4) combinations of hyperparameters
        {"n_estimators": [3, 10, 30], "max_features": [2, 4, 6, 8]},
        # then try 6 (2×3) combinations with bootstrap set as False
        {"bootstrap": [False], "n_estimators": [3, 10], "max_features": [2, 3, 4]},
    ]

    forest_reg = RandomForestRegressor(random_state=42)
    # train across 5 folds, that's a total of (12+6)*5=90 rounds of training
    grid_search = GridSearchCV(
        forest_reg,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        return_train_score=True,
    )
    logger.info("Running grid search on random forest...")
    grid_search.fit(X, y)

    grid_search.best_params_
    cvres = grid_search.cv_results_
    logger.info("Grid search complete, result: ")
    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        logger.info(f"{params}, Mean Score: {-mean_score}")
        print(np.sqrt(-mean_score), params)

    # feature_importances = grid_search.best_estimator_.feature_importances_
    # print(sorted(zip(feature_importances, X.columns), reverse=True))
    params_str = []
    for key, value in grid_search.best_params_.items():
        params_str.append(f"{key}-{value}")
    model_name = "forest-" + "-".join(params_str)

    housing_predictions = grid_search.best_estimator_.predict(X)
    forest_mse = mean_squared_error(y, housing_predictions)
    forest_rmse = np.sqrt(forest_mse)
    logger.info(
        f"Random forest model trained\n MSE : {forest_mse}\n RMSE: {forest_rmse}"
    )

    mlflow.log_params(grid_search.best_params_)
    mlflow.log_metric("tr_mse", forest_mse)
    mlflow.log_metric("tr_rmse", forest_rmse)
    mlflow.sklearn.log_model(
        grid_search.best_estimator_, "model", registered_model_name=model_name
    )

    return grid_search.best_estimator_, model_name


def main(**kwargs):
    """main funciton of train.py"""
    if kwargs.get("console_log"):
        setup_logger.add_log_handler(logger, logging.StreamHandler())
    if kwargs.get("log_path"):
        log_file = __file__.split("/")[-1] + ".log"
        complete_path = os.path.join(kwargs.get("log_path"), log_file)
        os.makedirs(os.path.dirname(complete_path), exist_ok=True)
        setup_logger.add_log_handler(logger, logging.FileHandler(complete_path, "a"))
    setup_logger.set_log_level(logger, kwargs.get("log_level"))

    X_train, y_train = load_training_data(kwargs.get("data_path"))
    train_linear_reg(X_train, y_train)
    train_decision_tree(X_train, y_train)
    train_forest_random_search(X_train, y_train)
    train_forest_grid_search(X_train, y_train)


def generate_argument_parser() -> argparse.ArgumentParser:
    """Returns argument parser for the script housing.train

    Returns
    -------
    argparse.ArgumentParser
        argument parser with required arguments added
    """
    parser = argparse.ArgumentParser(
        description="This script train different models (linear regression, decision tree, \
            random forest) on downloaded housing dataset and save them in disk for \
            future use"
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
