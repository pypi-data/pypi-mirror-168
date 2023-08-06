import os
import shutil

from unittest import TestCase

from yaml.scanner import ScannerError
from rkt_lib_toolkit.config import Config


class TestConfig(TestCase):
    def test_get_data(self):
        config = Config()
        config.data.clear()
        config.get_data(_config_dir="valid_config")

        assert config.data == {
            'valid_config': {'key1': {
                'sub_key': 'value',
                'sub_key2': 'value',
                'sub_key3': 'value',
                'sub_key4': 'value'
                }
            }
        }

    def test_get_data_dummy_data(self):
        config = Config()
        config.data.clear()
        try:
            config.get_data(_config_dir="dummy_config")
            self.fail("ScannerError expected here!")
        except ScannerError:
            assert config.data == {}

    def test_get_data_dummy_folder(self):
        config = Config()
        config.data.clear()
        config.get_data(_config_dir="missing_folder", create_if_not_exist=True)
        assert os.path.exists("missing_folder")
        shutil.rmtree("missing_folder")

    def test_get_data_from_specific_file(self):
        config = Config()
        config.data.clear()
        config.get_data(_config_dir="valid_config", needed_file="valid_config.yml")

        assert config.data == {
            'valid_config': {'key1': {
                'sub_key': 'value', 'sub_key2': 'value', 'sub_key3': 'value', 'sub_key4': 'value'
                }
            }
        }
