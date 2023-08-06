import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
from pywong.db.postgresql.utils import DbHelper
import warnings
import platform

# 忽略警告
warnings.filterwarnings('ignore')

"""
工作原理：
1）计算输入样本与训练样本之间的欧拉距离；
2）选取距离最近的k个训练样本，进行标签投票；
3）取票数最多的标签值作为输入样本的预测类别；
4）k为超参数，可使用网格搜索法寻找最优k。
"""


class KNNClassifier:
    """KNN分类器"""

    def __init__(self, name, k=2, is_normalize=True, path='D:\\model'):
        """构造函数"""
        assert k >= 1, "k must be valid"
        self.k = k
        # 模型名称
        self.name = name
        self.model_path = self.get_model_path(path)
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.X_train_standard = None
        self.X_test_standard = None
        self.model = KNeighborsClassifier(n_neighbors=self.k)
        self.normalizer = StandardScaler()
        self.is_normalize = is_normalize

    @staticmethod
    def feature(path):
        """私有方法，返回数据，仅内部使用"""
        data_all = pd.read_csv(path)
        feature = data_all.columns.values.tolist()
        return data_all, feature

    def fit(self, target, path=None, sql=None, data=None, test_size=0.2, random_state=666):
        """拟合数据"""
        data_all = None
        feature = None
        if path is not None:
            data_all, feature = self.feature(path)
            feature.remove(target)

        if sql is not None:
            data_all = DbHelper.execute_query_pd(sql)
            feature = data_all.columns.values.tolist()
            feature.remove(target)

        if data is not None:
            data_all = data
            feature = data_all.columns.values.tolist()
            feature.remove(target)

        # 切分训练集和测试集
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(np.array(data_all[feature]),
                                                                                np.array(data_all[[target]]),
                                                                                test_size=test_size,
                                                                                random_state=random_state)
        tmp = self.X_train
        if self.is_normalize:
            # 方差均值归一化
            self.normalizer.fit(self.X_train)
            self.X_train_standard = self.normalizer.transform(self.X_train)
            self.X_test_standard = self.normalizer.transform(self.X_test)

            tmp = self.X_train_standard

        self.model.fit(tmp, self.y_train.reshape(-1, ))

        return self

    def predict_inner(self):
        """预测"""
        return self.model.predict(self.__tmp())

    def predict_outer(self, path=None, sql=None, data=None, is_normalize=True):
        """预测外部输入"""
        data_all = None
        X_predict = None
        if path is not None:
            data_all, X_predict = self.feature(path)

        if sql is not None:
            data_all = DbHelper.execute_query_pd(sql)
            X_predict = data_all.columns.values.tolist()

        if data is not None:
            data_all = data
            X_predict = data_all.columns.values.tolist()

        tmp = np.array(data_all[X_predict])
        if is_normalize:
            tmp = self.normalizer.transform(tmp)
        return self.model.predict(tmp)

    def __tmp(self):
        """私有方法，返回临时数据，仅内部使用"""
        tmp = self.X_test
        if self.is_normalize:
            tmp = self.X_test_standard
        return tmp

    def score(self):
        """评估模型准确率"""
        return self.model.score(self.__tmp(), self.y_test.reshape(-1, ))

    def get_model_path(self, path):
        """返回模型路径"""
        file = None
        if not os.path.exists(path):
            os.mkdir(path)

        if 'Windows' == platform.system():
            file = f"{path}\\{self.name}.model"

        if 'Linux' == platform.system():
            file = f"{path}/{self.name}.model"

        return os.path.abspath(file)

    def save(self):
        """保存模型"""
        joblib.dump(self.model, self.model_path)
        print(f'保存{self.model_path}.')

    def load(self):
        """加载模型"""
        self.model = joblib.load(self.model_path)
        print(f"加载{self.name}.model.")

    def __str__(self):
        return "KNN(k={})".format(self.k)
