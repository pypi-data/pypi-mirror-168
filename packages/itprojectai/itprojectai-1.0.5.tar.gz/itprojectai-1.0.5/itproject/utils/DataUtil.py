from sklearn.datasets import load_boston, load_iris, load_breast_cancer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

"""数据集工具，获取波士顿房价，获取鸢尾花等数据集"""


def boston():
    """获取波士顿房价数据集exp: X,y = boston()"""
    data_url = "http://lib.stat.cmu.edu/datasets/boston"
    raw_df = pd.read_csv(data_url, sep="\\s+", skiprows=22, header=None)
    X = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    y = raw_df.values[1::2, 2]
    return X, y


def iris():
    """获取鸢尾花数据集exp: X,y = iris()"""
    return load_iris(return_X_y=True)


def cancer():
    """获取癌症预测数据集, 用于分析是良性还是恶性exp: X, y = cancer()"""
    return load_breast_cancer(return_X_y=True)


def split(X, y, test_percentage=0.20):
    """切分数据集,默认80%用于训练，20%用于测试,exp: split(X, y)"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_percentage)
    return X_train, X_test, y_train, y_test


def normalizing(arr, self=False):
    """归一化处理，把数据压缩在某个区间，如压缩在0-1之间"""
    if not self:
        mms = MinMaxScaler(feature_range=(0, 1))
        return mms.transform(arr)
    else:
        return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))


def standardizing(arr, self=False):
    """数据标准化处理,压缩到以0为中心的左右的范围"""
    if not self:
        ss = StandardScaler()
        return ss.transform(arr)
    else:
        (arr - arr.mean()) / arr.std()
