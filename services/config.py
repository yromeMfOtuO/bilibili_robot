import json
import os


class Config:
    """配置类从当前路径或者上级路径读取配置"""

    def __init__(self) -> None:
        # 获取config_path，向上寻找两级目录
        if os.path.exists('./config.json'):
            config_path = './config.json'
        elif os.path.exists('../config.json'):
            config_path = '../config.json'
        elif os.path.exists('../../config.json'):
            config_path = '../../config.json'
        else:
            raise Exception('未找到配置文件')

        with open(config_path) as f:
            load = json.load(f)
            print(load)
        self.properties = load

    def print(self):
        print(self.properties)


if __name__ == '__main__':
    config = Config()
    config.print()

