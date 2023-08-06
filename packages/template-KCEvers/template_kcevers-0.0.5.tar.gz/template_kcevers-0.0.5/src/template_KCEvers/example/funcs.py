import pathlib
import numpy as np


def test_path(x):
    return pathlib.Path(x)


def sum_of_squares(x):
    return np.sum(x**2)
