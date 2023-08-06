import pickle
import time
import os


class Data:
    """数据存储类"""

    def __init__(self, data_path):
        """数据类"""
        self.data_path = data_path

        self.status = 0  # 游戏状态
        self.score = 0  # 得分
        self.__start = 0  # 起始时间

        self.start()

    def start(self):
        """启动"""
        self.__start = time.time()
        return self.__start

    def get_time(self):
        """获取游戏的持续时间"""
        return time.time() - self.__start

    @property
    def time(self):
        return self.get_time()

    def save_data(self):
        """保存数据"""
        try:
            with open(self.data_path, "wb") as f:
                pickle.dump(self, f)
                print(f"{self.data_path}保存成功！")
                return 1
        except:
            print(f"{self.data_path}保存失败！")
            return 0

    @classmethod
    def load_data(cls, path) -> "Data":
        """加载数据"""
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
                assert isinstance(data, cls), type(data)
                return data
        except FileNotFoundError:
            # print(f'{path}不存在')
            return cls(path)

    def del_data(self):
        """删除数据"""
        try:
            os.remove(self.data_path)
            print(f"{self.data_path}删除成功")
            return 1
        except FileNotFoundError:
            # print(f'{self.data_path}不存在')
            return 0

    def __str__(self):
        return f"<Data stored in {self.data_path}>"

    __repr__ = __str__
