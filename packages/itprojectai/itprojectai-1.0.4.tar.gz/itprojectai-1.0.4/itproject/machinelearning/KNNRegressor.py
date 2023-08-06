import numpy as np


"""
    自定义KNN回归器
"""


class KNNRegressor(object):
    """
        自定义KNN回归器
         ....
    """

    def __init__(self, n_neighbors=5):
        """
            初始化函数
            - 超参数
        """
        self.n_neighbors = n_neighbors

    def fit(self, X, y):
        """
            训练过程
            传入：训练数据
        """

        self.X = np.array(X)
        self.y = np.array(y)

        # 参数校验
        if self.X.ndim != 2 or self.y.ndim != 1:
            raise Exception("训练数据的维度有错 ..")

    def predict(self, X):
        """
            预测过程
            传入：待预测的特征
            注意：批量预测

            1，找K个好友；
            2，取均值
        """
        # 类型转换
        X = np.array(X)

        # 参数校验
        if X.ndim != 2 or self.X.shape[1] != X.shape[1]:
            raise Exception("默认是批量预测，特征维度必须是二维的 ...")

        # 定义结果列表
        result = []

        # 计算过程
        for x in X:
            # 计算待测样本 x 和整个数据集中样本 self.X 的距离
            distances = np.sqrt(((self.X - x) ** 2).sum(axis=1))

            np.sqrt(((self.X - x) ** 2).sum(axis=1))

            # 找到K个最近的邻居
            idxes = np.argsort(distances)[:self.n_neighbors]
            # 求K个最近邻居的均值
            result.append(self.y[idxes].mean())

        # 返回结果
        return np.array(result)
