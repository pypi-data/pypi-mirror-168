import numpy as np
import example

def test_sum_of_squares():
    x = np.array([1,2,3])
    return example.sum_of_squares(x)

def test_paths():
    return example.test_path("C:\\")