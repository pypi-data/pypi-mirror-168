import os

from rkt_lib_toolkit.tool import Tool, Singleton

obj = Tool()


class FakeClass(metaclass=Singleton):
    def __init__(self):
        self.name = "singleton"


class TestTool:
    def test_formatted_from_os(self):
        if os.name == "nt":
            excepted = obj.formatted_from_os(os.getcwd()).endswith("\\")
        else:
            excepted = obj.formatted_from_os(os.getcwd()).endswith("/")
        assert excepted

    def test_get_cwd(self):
        assert obj.get_cwd() == f"{os.getcwd()}\\" if os.name == "nt" else f"{os.getcwd()}/"

    def test_get_dir_flat(self):
        if os.name == "nt":
            excepted = f"{os.getcwd()}\\tests\\"
        else:
            excepted = f"{os.getcwd()}/tests/"
        assert obj.get_dir("tests") == excepted

    def test_get_dir_recursive(self):
        if os.name == "nt":
            excepted = f"{os.getcwd()}\\tests\\resources\\"
        else:
            excepted = f"{os.getcwd()}/tests/resources/"

        assert obj.get_dir("resources") == excepted


class TestSingleton:
    def test_singleton(self):
        obj_1 = FakeClass()
        obj_2 = FakeClass()
        assert obj_1 == obj_2

