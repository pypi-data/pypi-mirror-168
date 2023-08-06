from prophet import Prophet
import pandas as pd
import joblib
import os
from pywong.db.postgresql.utils import DbHelper
import warnings
import platform

# 忽略警告
warnings.filterwarnings('ignore')

"""
工作原理：
根据时间预测结果
"""


class TimeSeriesProphet:
    """时间序列"""

    def __init__(self, name, path='D:\\model'):
        """构造函数"""
        self.future = None
        self.forecast = None
        self.data = None
        # 模型名称
        self.name = name
        self.model_path = self.get_model_path(path)
        self.model = Prophet()

    def fit(self, path=None, sql=None, data=None):
        """拟合数据"""
        data_all = None
        if path is not None:
            data_all = pd.read_csv(path)

        if sql is not None:
            data_all = DbHelper.execute_query_pd(sql)

        if data is not None:
            data_all = data

        self.data = data_all

        self.model.fit(self.data)

        return self

    def make_future(self, periods, freq, include_history):
        """构造预测数据"""
        future = self.model.make_future_dataframe(periods=periods, freq=freq, include_history=include_history)
        self.future = future

    def predict(self, periods, freq, include_history=False):
        """预测"""
        self.make_future(periods, freq, include_history)
        forecast = self.model.predict(self.future)
        self.forecast = forecast

        return forecast

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
        return "TimeSeriesProphet()"
