import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os
from pywong.db.postgresql.utils import DbHelper
import warnings
import platform

# 忽略警告
warnings.filterwarnings('ignore')

"""
工作原理：
1）最优化损失函数，转换为求函数极值问题，即在导数为0处能够取得极大值或者极小值；
1）根据训练样本计算截距和系数；
3）评价指标：R2，越大越好，最大为1；小于0，表示可能不存在线性关系；
4）不需要对样本数据进行归一化处理。
"""


class MLinearRegression:
    """线性回归器"""

    def __init__(self, name, path='D:\\model'):
        """构造函数"""
        # 系数
        self.coef_ = None
        # 截距
        self.intercept_ = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.model = LinearRegression()
        # 模型名称
        self.name = name
        self.model_path = self.get_model_path(path)

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

        self.model.fit(self.X_train, self.y_train.reshape(-1, ))

        self.coef_ = self.model.coef_
        self.intercept_ = self.model.intercept_

        return self

    def predict_inner(self):
        """预测"""
        return self.model.predict(self.X_test)

    def predict_outer(self, path=None, sql=None, data=None):
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

        return self.model.predict(np.array(data_all[X_predict]))

    def score(self):
        """评估模型准确率"""
        return self.model.score(self.X_test, self.y_test.reshape(-1, ))

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
        return "MLinearRegression()"
