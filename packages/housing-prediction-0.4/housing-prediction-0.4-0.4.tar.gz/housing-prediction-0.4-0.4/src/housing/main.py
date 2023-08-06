import argparse
import configparser
import os

import mlflow

from housing import mlflow_utils
from housing.ingest_data import main as ingest_data
from housing.score import main as score
from housing.train import main as train


def generate_argument_parser() -> argparse.ArgumentParser:
    """Returns argument parser for the housing package

    Returns
    -------
    argparse.ArgumentParser
        argument parser with required arguments added
    """
    parser = argparse.ArgumentParser(
        description="This script train various models, and score \
            them on https://raw.githubusercontent.com/ageron/handson-ml/master/ \
            \
            This script runs housing.ingest_data, housing.train and housing.score \
            scripts"
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


@mlflow_utils.mlflow_conf
@mlflow_utils.mlflow_start_run
def run():
    """The entry point of the script"""
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

    ingest_data(**params)
    train(**params)
    # end the mlflow run
    mlflow.end_run()
    score(**params)
