import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import os
from pywong.db.postgresql.utils import DbHelper
import warnings
import platform

# 忽略警告
warnings.filterwarnings('ignore')

"""
工作原理：
1）随机森林集成多个决策树，每个决策树基于随机样本进行训练，即吸收了决策树和Bagging分类器的优点；
2）每个决策树在随机特征子集上寻找最优划分，并非所有特征，用于增加子模型的随机性。
"""


class RandomForest:
    """随机森林"""

    def __init__(self, name, n_estimators=500, is_reg=True, path='D:\\model'):
        """构造函数，默认用于回归任务"""
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.model = None
        # 模型名称
        self.name = name
        self.model_path = self.get_model_path(path)
        self.is_reg = is_reg

        if self.is_reg:
            self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=666, oob_score=True, n_jobs=-1)
        else:
            self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=666, oob_score=True, n_jobs=-1)

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
        return self.model.oob_score_

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
        if self.is_reg:
            name = "RandomForestRegressor"
        else:
            name = "RandomForestClassifier"
        return "{}()".format(name)
