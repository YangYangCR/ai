import dataclasses
from abc import abstractmethod, ABC
from collections import defaultdict

import sys


@dataclasses.dataclass
class Animal(ABC):
    name: str = None
    type: str = None

    def __init__(self, name):
        pass

    @abstractmethod
    def run(self):
        pass

    @classmethod
    def show(cls, name):
        pass

    @staticmethod
    def walk(self):
        pass


class Dog(Animal):

    def __init__(self, name: str):
        super().__init__(name)
        print("this is dog")

    @property
    def run(self):
        print("dog run")
        return "100"


@dataclasses.dataclass(frozen=True)
class Cat():
    name: str
    age: int

    def __init__(self, name: str):
        pass

    def run(self):
        pass


class Gen:

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        pass

    def __repr__(self):
        """开发人员友好的表示"""
        return f"Gen('{self.name}', {self.age})"

    def __str__(self):
        """用户友好的表示"""
        return f"{self.name} ({self.age}岁)"


class PipelineState:

    def __init__(self, pip_id):
        self.pip_id = pip_id
        self.processes = []  # 子进程列表
        self.state = "init"  # init / running / fail
        self.error = None

    def add_process(self, p):
        self.processes.append(p)

    def set_running(self):
        self.state = "running"

    def set_fail(self, err):
        self.state = "fail"
        self.error = err

    def __repr__(self):
        return f"PipelineState(state={self.state}, processes={len(self.processes)}, error={self.error})"


def data():
    yield 1, 100, 200


def get_user_info():
    yield "Alice", 25, "alice@email.com"


def multi_data():
    yield 1, 2, 3
    yield 4, 5, 6
    yield 7, 8, 9


import zmq
import socket as st


def bind_to_specific_ip():
    """绑定到具体 IP 地址"""
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # 获取本机具体 IP
    hostname = st.gethostname()
    print("hostname:", hostname)
    local_ip = st.gethostbyname(hostname)

    # 直接绑定到具体 IP
    port = socket.bind_to_random_port(f"tcp://{local_ip}")

    # 获取完整地址（现在会是具体 IP）
    full_address = socket.getsockopt_string(zmq.LAST_ENDPOINT)

    print(f"本机 IP: {local_ip}")
    print(f"绑定端口: {port}")
    print(f"完整地址: {full_address}")  # tcp://192.168.1.100:56789

    return socket, full_address


def gen() -> str:
    return "==="


if __name__ == "__main__":
    # bind_to_specific_ip()
    dog = Dog("dh")
    data = dog.run
    # dict_ = defaultdict(lambda: PipelineState("10"))
    dict_ = defaultdict(lambda: Gen("Tom", 10))
    # dict_["name"] = "jerry"
    # print(dict_["name"])
    print(dict_["age"](10))

    # name_dict = {"k1": "v1", "k2": "v2"}
    # cmd1 = []
    # for key, value in name_dict:
    #     cmd1.append(key)
    #     cmd1.append(value)
    # print(cmd1)
    #
    # cmd2 = [sys.executable, "-m", "pytest", "test"]
    # print(cmd1 + cmd2)
    #
    # assert 1 > 2, "==="
