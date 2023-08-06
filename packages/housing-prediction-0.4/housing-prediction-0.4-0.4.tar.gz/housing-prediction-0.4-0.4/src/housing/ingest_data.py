import argparse
import configparser
import logging
import os
import tarfile

import numpy as np
import pandas as pd
from six.moves import urllib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from housing import setup_logger, sklearn_utils
from housing.transformers import CombinedAttributesAdder

logger = logging.getLogger(__file__)


def download_data(download_path: str):
    """Download housing price dataset (.tgz) in <download_path>/raw
    and call extract_data to extract the downloaded tar file

    Parameters
    ----------
    download_path : str
        directory path to store the downloaded and extracted files
    """
    DOWNLOAD_WEB_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
    HOUSING_URL = DOWNLOAD_WEB_ROOT + "datasets/housing/housing.tgz"
    RAW_DOWNLOAD_PATH = os.path.join(download_path, "raw")
    os.makedirs(RAW_DOWNLOAD_PATH, exist_ok=True)
    tgz_path = os.path.join(RAW_DOWNLOAD_PATH, "housing.tgz")
    result = urllib.request.urlretrieve(HOUSING_URL, tgz_path)
    logger.info(f"Downloaded {result[0]}")
    extract_data(download_path, tgz_path)


def extract_data(download_path: str, tgz_path: str):
    """Extract tar file in <download_path>/raw

    Parameters
    ----------
    download_path : str
        location of data directory

        if tar file is located in data/raw/ , then download_path should be 'data'

    tgz_path : str
        path of downloaded tar dataset file, example: data/raw/housing.tgz
    """
    RAW_DOWNLOAD_PATH = os.path.join(download_path, "raw")
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=RAW_DOWNLOAD_PATH)
    housing_tgz.close()
    logger.info(f"Data extracted to {RAW_DOWNLOAD_PATH}")


def load_housing_data(data_path: str) -> pd.DataFrame:
    """Load extracted dataset (.csv) <data_path>/housing.csv

    Parameters
    ----------
    data_path : str
        location of extracted housing.csv dataset,
        example: data/raw

    Returns
    -------
    pd.DataFrame
        Dataframe of extracted dataset
    """
    csv_path = os.path.join(data_path, "housing.csv")
    return pd.read_csv(csv_path)


def split_data(housing: pd.DataFrame) -> tuple([pd.DataFrame, pd.DataFrame]):
    """Split extracted data into training and validation sets

    Parameters
    ----------
    housing : pd.DataFrame
        the original housing dataframe

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        training, and validation dataframes respectively
    """
    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
        labels=[1, 2, 3, 4, 5],
    )
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(housing, housing["income_cat"]):
        strat_train_set = housing.loc[train_index]
        strat_test_set = housing.loc[test_index]
    for set_ in (strat_train_set, strat_test_set):
        set_.drop("income_cat", axis=1, inplace=True)
    logger.info(
        (
            "Data splited into train and val set\n"
            f"Training shape:{strat_train_set.shape}\n"
            f"Validation shape:{strat_test_set.shape}"
        )
    )
    return (strat_train_set, strat_test_set)


def generate_transformer_pipeline(num_attribs: list, cat_attribs: list, cat_labels: list) -> ColumnTransformer:
    """returns a column transformer which will be used to apply pre-processing on the data

    Parameters
    ----------
    num_attribs : list
        list of column names having numerical data
    cat_attribs : list
        list of column names having categorical data
    cat_labels : list
        list of unique categories in <cat_attribs>

    Returns
    -------
    ColumnTransformer
        column transforer for performing imputation, creating new features, one hot encoding
    """
    transformer_pipeline = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("attribs_adder", CombinedAttributesAdder()),
                    ]
                ),
                num_attribs,
            ),
            (
                "cat",
                OneHotEncoder(categories=[cat_labels]),
                cat_attribs,
            ),
        ]
    )
    return transformer_pipeline


def split_transform_data(download_path: str) -> tuple([str, str]):
    """Split the dataset present in <download_path>/raw into traning and
    validation set by calling split_data, and apply preprocesing
    (cleaning, feature engineering) on both dataframes (training, validation sets)

    The processed files are then stored in <download_path>/processed directory

    Parameters
    ----------
    download_path : str
        directory where data files are located

        if data files are located in data/raw, then 'data' should be passed

    Returns
    -------
    tuple[str, str]
        locations where the traning and validation
        datasets are stored respectivelty.

        example: data/processed/train_housing.csv, data/processed/val_housing.csv,
    """
    RAW_DOWNLOAD_PATH = os.path.join(download_path, "raw")
    PROCESSED_DOWNLOAD_PATH = os.path.join(download_path, "processed")
    os.makedirs(PROCESSED_DOWNLOAD_PATH, exist_ok=True)

    # loading raw dataset and spliting
    housing = load_housing_data(RAW_DOWNLOAD_PATH)
    strat_train_set, strat_test_set = split_data(housing)

    housing = strat_train_set.drop("median_house_value", axis=1)  # drop labels for training set
    housing_labels = strat_train_set["median_house_value"].copy()

    # creating transformation pipeline
    transformer_pipeline = generate_transformer_pipeline(
        housing.drop("ocean_proximity", axis=1).columns,
        ["ocean_proximity"],
        housing.ocean_proximity.unique(),
    )

    # fitting pipeline and transforming data
    housing_prepared_values = transformer_pipeline.fit_transform(housing)
    prepared_columns = sklearn_utils.get_feature_names_from_column_transformer(transformer_pipeline)
    housing_prepared = pd.DataFrame(housing_prepared_values, housing.index, prepared_columns)

    # repeating steps for test set by using .transform() on pipeline
    X_test = strat_test_set.drop("median_house_value", axis=1)
    y_test = strat_test_set["median_house_value"].copy()

    X_test_prepared_values = transformer_pipeline.fit_transform(X_test)
    X_test_prepared = pd.DataFrame(X_test_prepared_values, X_test.index, prepared_columns)

    # Joining X, y as train and val dataset, and saving to disk
    train_dataset = housing_prepared.join(housing_labels)
    val_dataset = X_test_prepared.join(y_test)
    logger.info(f"Created new features, now there are {train_dataset.shape[1]} features")

    train_data_path = os.path.join(PROCESSED_DOWNLOAD_PATH, "train_housing.csv")
    val_data_path = os.path.join(PROCESSED_DOWNLOAD_PATH, "val_housing.csv")
    train_dataset.to_csv(train_data_path)
    val_dataset.to_csv(val_data_path)
    logger.info(f"Training and validation dataset saved to {PROCESSED_DOWNLOAD_PATH}")
    return train_data_path, val_data_path


def main(**kwargs):
    """main funciton of ingest_data.py"""
    if kwargs.get("console_log"):
        setup_logger.add_log_handler(logger, logging.StreamHandler())
    if kwargs.get("log_path"):
        log_file = __file__.split("/")[-1] + ".log"
        complete_path = os.path.join(kwargs.get("log_path"), log_file)
        os.makedirs(os.path.dirname(complete_path), exist_ok=True)
        setup_logger.add_log_handler(logger, logging.FileHandler(complete_path, "a"))
    setup_logger.set_log_level(logger, kwargs.get("log_level"))

    tgz_path = os.path.join(kwargs.get("data_path"), "raw", "housing.tgz")

    if os.path.isfile(tgz_path):
        extract_data(kwargs.get("data_path"), tgz_path)
    else:
        download_data(kwargs.get("data_path"))

    split_transform_data(kwargs.get("data_path"))


def generate_argument_parser() -> argparse.ArgumentParser:
    """Returns argument parser for the script housing.ingest_data

    Returns
    -------
    argparse.ArgumentParser
        argument parser with required arguments added
    """
    parser = argparse.ArgumentParser(
        description="This script downloads the data from \
            https://raw.githubusercontent.com/ageron/handson-ml/master/ , extract the \
            tar file, split into training and validation datasets, and apply \
            pre-processing."
    )
    parser.add_argument("-d", "--data_path", type=str, help="Path for the data folder (raw & processed)")
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
