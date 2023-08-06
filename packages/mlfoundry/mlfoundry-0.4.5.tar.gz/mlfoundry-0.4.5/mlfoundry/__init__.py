import logging
import sys

from mlflow.entities import Feature

from mlfoundry.enums import *
from mlfoundry.log_types import Image, Plot
from mlfoundry.log_types.artifacts.model import CustomMetric, ModelSchema, ModelVersion
from mlfoundry.login import login
from mlfoundry.mlfoundry_api import get_client
from mlfoundry.mlfoundry_run import MlFoundryRun
from mlfoundry.monitoring.entities import Actual, Prediction, PredictionData
from mlfoundry.schema import Schema
from mlfoundry.version import __version__

__all__ = [
    "FileFormat",
    "ModelFramework",
    "DataSlice",
    "ModelType",
    "Schema",
    "get_client",
    "__version__",
    "MlFoundryRun",
    "login",
    "Image",
    "Plot",
    "Prediction",
    "PredictionData",
    "Actual",
    "Feature",
    "ModelSchema",
    "ModelVersion",
    "CustomMetric",
]


def _configure_logger(level):
    # TODO (chiragjn): This is just a temporary way to configure logging.
    #                  Need to move it in client or run init with option to set verbosity
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter(
            "[mlfoundry] %(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False


_configure_logger(logging.INFO)
