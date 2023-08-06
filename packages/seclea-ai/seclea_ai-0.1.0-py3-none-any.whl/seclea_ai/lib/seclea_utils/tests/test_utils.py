import os.path
import unittest

import pandas as pd

from ..dataset_management.dataset_utils import (
    get_dataset_hash,
    get_dataset_project_hash,
    get_project_hash,
)


class TestFileCompressor(unittest.TestCase):
    class Project:
        ...

    def setUp(self) -> None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.folder_path = os.path.join(base_dir, "tests")
        self.dataset = f"{self.folder_path}/example_files/filled_na_train.csv"
        self.df = pd.read_csv(self.dataset)
        self.series = self.df["DeviceType"]

    def test_get_dataset_project_hash(self):
        hash = get_dataset_project_hash(
            dataset=self.series,
            project=self.Project(),
        )
        self.assertIsInstance(hash, str)

    def test_get_dataset_hash(self):
        hash = get_dataset_hash(
            dataset=self.series,
        )
        self.assertIsInstance(hash, str)

    def test_get_project_hash(self):
        hash = get_project_hash(
            project=self.Project(),
        )
        self.assertIsInstance(hash, str)
