import os
import uuid
from io import StringIO
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from ..core import CompressionFactory, load_object, save_object


def save_dataset(dataset, file_name, path):
    """
    To be extended to support datasets other than csv.
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    tmp_path = os.path.join(path, uuid.uuid4().__str__())
    dataset.to_csv(tmp_path, index=True)
    rb = open(tmp_path, "rb")
    save_path = save_object(rb, file_name=file_name, path=path, compression=CompressionFactory.ZSTD)
    rb.close()
    os.remove(tmp_path)
    return save_path


def load_dataset(dataset_path: str, index_col=None):
    """
     # TODO: Extend to different types of datasets
    :param model_dataset:
    :return:
    """

    dataset_str = load_object(dataset_path, as_bytes=False)
    dataset_stream = StringIO(dataset_str)
    df = pd.read_csv(dataset_stream, index_col=index_col)
    return df


def column_hash(dataset: DataFrame) -> int:
    """Invariant to ordering of columns/rows"""
    sum = 0
    for col in dataset.columns:
        sum += int(pd.util.hash_pandas_object(dataset[col]).sum())
    return sum


def dataset_hash(dataset, project_id: str) -> str:
    return str(hash(column_hash(dataset) + hash(project_id)))


def get_dataset_project_hash(dataset, project) -> str:
    return str(hash(bytes(dataset)) + hash(project))


def get_dataset_hash(dataset) -> str:
    return str(hash(bytes(dataset)))


def get_project_hash(project) -> str:
    return str(hash(project))
