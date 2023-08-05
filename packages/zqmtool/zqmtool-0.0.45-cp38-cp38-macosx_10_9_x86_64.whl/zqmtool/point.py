import numpy as np


def move_left_upper_2d_point_to_zero(x):
    x_trans = np.amin(x[:, 0])
    y_trans = np.amin(x[:, 1])
    x[:, 0] -= x_trans
    x[:, 1] -= y_trans
    return x, x_trans, y_trans





