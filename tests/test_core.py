import os

import numpy as np
import pytest

from matpowercaseframes import CaseFrames
from matpowercaseframes.idx import BUS_I, BUS_TYPE

"""
    pytest -n auto -rA --lf -c pyproject.toml --cov-report term-missing --cov=matpowercaseframes tests/
"""

CASE_NAME = "case9.m"
CURDIR = os.path.realpath(os.path.dirname(__file__))
CASE_DIR = os.path.join(os.path.dirname(CURDIR), "data")
CASE_PATH = os.path.join(CASE_DIR, CASE_NAME)


def test_input_str_path():
    CaseFrames(CASE_PATH)


def test_input_oct2py_io_Struct():
    from matpower import start_instance

    m = start_instance()

    # before run
    mpc = m.loadcase("case9", verbose=False)
    CaseFrames(mpc)

    # after run
    mpc = m.runpf(mpc, verbose=False)
    CaseFrames(mpc)

    m.exit()


def test_input_type_error():
    with pytest.raises(TypeError):
        CaseFrames(1)


def test_read_value():
    cf = CaseFrames(CASE_PATH)

    assert cf.version == "2"
    assert cf.baseMVA == 100

    narr_gencost = np.array(
        [
            [2.000e00, 1.500e03, 0.000e00, 3.000e00, 1.100e-01, 5.000e00, 1.500e02],
            [2.000e00, 2.000e03, 0.000e00, 3.000e00, 8.500e-02, 1.200e00, 6.000e02],
            [2.000e00, 3.000e03, 0.000e00, 3.000e00, 1.225e-01, 1.000e00, 3.350e02],
        ]
    )
    assert np.allclose(cf.gencost, narr_gencost)

    narr_bus = np.array(
        [
            [1, 3, 0, 0, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
            [2, 2, 0, 0, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
            [3, 2, 0, 0, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
            [4, 1, 0, 0, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
            [5, 1, 90, 30, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
            [6, 1, 0, 0, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
            [7, 1, 100, 35, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
            [8, 1, 0, 0, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
            [9, 1, 125, 50, 0, 0, 1, 1, 0, 345, 1, 1.1, 0.9],
        ]
    )
    assert np.allclose(cf.bus, narr_bus)
    assert np.allclose(cf.bus["BUS_I"], narr_bus[:, BUS_I])
    assert np.allclose(cf.bus["BUS_TYPE"], narr_bus[:, BUS_TYPE])

    # TODO:
    # Check all data


def test_read_case_name():
    cf = CaseFrames(CASE_PATH)
    assert cf.name == "case9"


def test_get_attributes():
    cf = CaseFrames(CASE_PATH)
    assert cf.attributes == ["version", "baseMVA", "bus", "gen", "branch", "gencost"]

    with pytest.raises(AttributeError):
        cf.attributes = ["try", "replacing", "attributes"]

    # TODO: protect from attributes changed by user
    # cf.attributes[0] = 'try'
    # print(cf.attributes[0])
    # print(cf.attributes)


def test_to_xlsx():
    cf = CaseFrames(CASE_PATH)
    cf.to_excel("tests/results/test_to_xlsx.xlsx")


def test_to_csv():
    cf = CaseFrames(CASE_PATH)
    cf.to_csv("tests/results")


def test_to_dict():
    cf = CaseFrames(CASE_PATH)
    cf.to_dict()


def test_to_mpc():
    cf = CaseFrames(CASE_PATH)
    cf.to_mpc()
