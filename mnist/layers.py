from __future__ import print_function
import numpy as np


def sigmoid_double(x):
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid(z):
    return np.vectorize(sigmoid_double)(z)
