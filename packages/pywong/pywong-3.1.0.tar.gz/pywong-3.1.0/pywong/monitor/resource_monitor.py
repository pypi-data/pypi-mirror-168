"""
资源监测
"""
import psutil


class Resource:
    """资源类"""
    def __init__(self):
        """构造函数"""
        self.memory = Memory()
        self.cpu = CPU()
        self.hard_disk = HardDisk()

    def get_all(self):
        """获取所有信息"""
        self.get_memory()
        self.get_cpu()
        self.get_hard_disk()

    def get_memory(self):
        """获取内存信息"""
        self.memory.get_memory_info()

    def get_cpu(self):
        """获取CPU信息"""
        self.cpu.get_cpu_nfo()

    def get_hard_disk(self):
        """获取磁盘信息"""
        self.hard_disk.get_hard_disk_info()


class Memory:
    """内存类"""
    def __init__(self):
        """构造函数"""
        self.total = None
        self.used = None
        self.free = None
        self.available = None
        self.percent = None

        self.get_memory_info()

    def get_memory_info(self):
        """获取内存信息"""
        memory = psutil.virtual_memory()
        self.total = memory.total
        self.used = memory.used
        self.free = memory.free
        self.available = memory.available
        self.percent = memory.percent

    def __str__(self):
        return "Memory usage rate: {}%".format(self.percent)

    def __repr__(self):
        return self.__str__()


class CPU:
    """CPU类"""
    def __init__(self):
        """构造函数"""
        self.logical_count = None
        self.physical_count = None
        self.usage_rate = None
        self.user_time = None
        self.io_wait_time = None

        self.get_cpu_nfo()

    def get_cpu_nfo(self):
        """获取CPU信息"""
        self.logical_count = psutil.cpu_count(logical=True),
        self.physical_count = psutil.cpu_count(logical=False),
        self.usage_rate = psutil.cpu_percent(),
        self.user_time = psutil.cpu_times().user,

    def __str__(self):
        return "CPU usage rate: {}%".format(self.usage_rate[0])

    def __repr__(self):
        return self.__str__()


class HardDisk:
    """磁盘类"""
    def __init__(self):
        """构造函数"""
        self.disk_partition = None
        self.disk_usage = None
        self.io_counters = None

        self.get_hard_disk_info()

    def get_hard_disk_info(self):
        """获取磁盘信息"""
        self.disk_partition = psutil.disk_partitions()
        self.disk_usage = [psutil.disk_usage(d.device) for d in self.disk_partition]
        self.io_counters = psutil.disk_io_counters()

    @staticmethod
    def get_hard_disk_usage(path):
        """获取磁盘使用率"""
        # noinspection PyBroadException
        try:
            return psutil.disk_usage(path)
        except Exception as e:
            return e.__str__()

    @staticmethod
    def get_io_counters(disk=True):
        """获取IO数"""
        return psutil.disk_io_counters(perdisk=disk)

    def __str__(self):
        res = ""
        try:
            for d in range(len(self.disk_partition)):
                item_str = "HardDisk {} usage rate: {}%".format(self.disk_partition[d].device,
                                                                self.disk_usage[d].percent)
                res = res + item_str + "\n"
            return res
        except Exception as e:
            return e.__str__()

    def __repr__(self):
        return self.__str__()