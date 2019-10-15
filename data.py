from typing import Optional
import numpy as np


def divide_ds(data: np.ndarray, label: Optional[np.ndarray] = None,
              train_per: float = 0.8):


    index = int(len(data) * train_per)

    train_x = data[:index]
    test_x = data[index:]

    train_y, test_y = None, None
    if label is not None:
        train_y = label[:index]
        test_y = label[index:]

    return train_x, test_x, train_y, test_y