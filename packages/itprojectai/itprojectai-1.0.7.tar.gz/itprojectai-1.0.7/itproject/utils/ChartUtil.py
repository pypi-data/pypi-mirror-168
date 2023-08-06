from matplotlib import pyplot as plt

"""数据可视化工具，可以用于预测结果定性分析"""


def plot(X, y):
    """绘制折线图"""
    plt.plot(X, y)
    plt.show()


def scatter(X, y):
    """绘制散点图"""
    plt.scatter(X, y)
    plt.show()


def scatterX(X):
    """绘制散点图, 只需要传入某个特征"""
    plt.scatter(range(X.size), X)
