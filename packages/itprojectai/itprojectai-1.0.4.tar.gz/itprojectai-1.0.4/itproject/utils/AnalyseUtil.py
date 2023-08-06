import numpy as np

"""预测结果定性分析，MAE,MSE等等"""


def mae(y_pred, y_test):
    """预测结果y_pred和实际数据y_test的平均绝对误差MAE, 用这种方式衡量，求导数是麻烦事"""
    return np.abs(y_pred - y_test).mean()


def mse(y_pred, y_test):
    """预测结果y_pred和实际数据y_test的均方差，解决MAE求导数麻烦的问题
    回归问题一般都是用MSE来衡量误差的
    """
    return ((y_pred - y_test) ** 2).mean()
