import multiprocessing
from multiprocessing.process import BaseProcess


class Proxy:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        print(f"代理访问: {name}")
        return getattr(self._obj, name)


# 使用
class Real:
    def greet(self):
        return "Hello, World!"

class Demo:

    def __init__(self):
        print("init demo")

    def __getattr__(self, name):
        print(f"属性 '{name}' 不存在，调用 __getattr__")
        return f"动态创建的 {name}"


def show_name(name: str):
    print("name is " + name)


if __name__ == '__main__':
    # context = multiprocessing.get_context("spawn")
    # process: BaseProcess = context.Process(target=show_name, name="show name", kwargs={"name": "Tom"})
    # process.start()
    # process.join()
    real = Real()
    proxy = Proxy(real)
    proxy.greet()

    multiprocessing.Queue
    multiprocessing.Pipe
    multiprocessing.connection.Connection
