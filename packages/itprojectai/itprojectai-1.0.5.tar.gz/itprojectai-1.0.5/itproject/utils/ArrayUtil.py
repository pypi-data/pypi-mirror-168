import numpy as np

"""一维数组/向量的运算，加减乘除，平均值，标准差，方差等等"""


def getArray(n):
    """获取n个数字的一维数组"""
    return np.arange(n)


def getArrayByZone(start=None, *args, **kwargs):
    """获取指定区间的数组，并且指定每个数之间的间隔, step为负数表示反方向生成
    exp: getArrayByZone(start=1,stop=12,step=2)"""
    return np.arange(start=start, *args, **kwargs)


def getArrayByCount(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
                    axis=0):
    """指定某个区间，指定要生成多少个数，产生等间隔的数列
    exp: arr1 = getArrayByCount(start=1, stop=12, num=12)
    """
    return np.linspace(start=start, stop=stop, num=num, endpoint=True, retstep=False, dtype=None,
                       axis=0)


def getArrayAvg(arr):
    """求数组的平均值"""
    return np.array(arr).mean()


def getArrayStd(arr):
    """求数组的标准差"""
    return np.array(arr).std()


def getArrayVar(arr):
    """求数组的方差"""
    return np.array(arr).var()


def getArraySize(arr):
    """求数组的长度"""
    return np.array(arr).size


def getArrayShape(arr):
    """求数组的形状"""
    return np.array(arr).shape


def getArrayNDim(arr):
    """求数组的维度"""
    return np.array(arr).ndim


def getArrayMod(arr):
    """求向量的模，模就是向量的长度, 模=平方和开根号"""
    return np.sqrt((np.array(arr) ** 2).sum())


def getArrayDot(arr1, arr2):
    """求两个向量的点乘积, 即两个向量的内积"""
    return np.array(arr1).dot(np.array(arr2))


def sort(arr, axis=-1, kind=None, order=None):
    """数组排序："""
    return np.array(arr).argsort(axis=axis, kind=kind, order=order)


def distance(X1, X2):
    """计算两个向量之间的距离，距离越近表示这两个向量越相似, 初中知识是两点之间的距离
    高维空间里称为欧几里得距离，也叫欧氏距离
    exp:
    X = np.array([1,2,3])
    X1 = np.array([4,5,6])
    ArrayUtil.distance(X, X1)
    """
    return np.sqrt(((X1 - X2) ** 2).sum())


def cos(X1, X2):
    """计算两个向量的余弦相似度，两个向量的夹角越小，表示越相似"""
    return X1 @ X2 / np.linalg.norm(X1) / np.linalg.norm(X2)


def pierxun(X1, X2):
    """皮尔逊相关系数，本质也是余弦相似度，也是用来衡量两个向量的相似度"""
    pass
