from typing import Optional
import numpy as np


def split_data(data, label = None, train_per: float = 0.8):
    """

    :param data: array_like
    :param label: array_like
    :param train_per: float
    :return:
    """

    index = int(len(data) * train_per)

    train_x = data[:index]
    test_x = data[index:]

    if label is None:
        return train_x, test_x

    train_y = label[:index]
    test_y = label[index:]
    return train_x, test_x, train_y, test_y

