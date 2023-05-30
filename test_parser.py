import pytest
from scanner import Scanner, Symbol, ErrorCodes
from names import Names
from parse import *


@pytest.fixture
def test_names():
    names = Names()
    return names


@pytest.fixture
def test_file_1():
    path = "tests/parser/test1.txt"
    return path


@pytest.fixture
def test_file_2():
    path = "tests/parser/test2.txt"
    return path