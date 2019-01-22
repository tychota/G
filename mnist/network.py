from __future__ import print_function
from six.moves import range
import random
import numpy as np


class MSE:  # <1>

    def __init__(self):
        pass

    @staticmethod
    def loss_function(predictions, labels):
        diff = predictions - labels
        return 0.5 * sum(diff * diff)[0]  # <2>

    @staticmethod
    def loss_derivative(predictions, labels):
        return predictions - labels
