from pyod.models.cof import COF


class AbnormalCOF:
    """异常值检测"""

    def __init__(self, data):
        """构造函数"""
        self.data = data

    def fit_predict(self):
        """异常值检测"""
        cof = COF()
        col = self.data.columns
        cof_label = cof.fit_predict(self.data)
        # 标签为1的为异常值
        self.data['label'] = cof_label
        # 获取处理后的正常数据
        self.data = self.data[self.data.label != 1][col]
        return self.data
