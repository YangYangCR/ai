import os
import signal
import sys
from multiprocessing import Process, Queue
import time
import random
import select

import zmq


def producer(q, name):
    """生产者函数"""
    for i in range(5):
        item = f"{name}-产品{i}"
        q.put(item)
        print(f"生产者 {name} 生产了: {item}")
        time.sleep(random.random())

    # 发送结束信号
    q.put(None)


def consumer(q, name):
    """消费者函数"""
    while True:
        item = q.get()
        if item is None:  # 收到结束信号
            print(f"消费者 {name} 收到结束信号，退出")
            break
        print(f"消费者 {name} 消费了: {item}")
        time.sleep(random.random() * 2)


def process1():
    print(f"child self {os.getpid()}")
    print(f"child patent {os.getppid()}")

    # print(f"child group id {os.getpgid(os.getpid())}")

    def handle_child_exit(signum, frame):
        print(f"child self exit {signum}...")

    # kill(kill -9不生效)
    signal.signal(signal.SIGTERM, handle_child_exit)
    # ctrl + c
    signal.signal(signal.SIGINT, handle_child_exit)
    time.sleep(10)
    print(f"child1 finished")
    return "process1"


def process2():
    print(f"child self {os.getpid()}")
    print(f"child patent {os.getppid()}")

    # print(f"child group id {os.getpgid(os.getpid())}")

    def handle_child_exit(signum, frame):
        print(f"child self exit {signum}...")

    # kill(kill -9不生效)
    signal.signal(signal.SIGTERM, handle_child_exit)
    # ctrl + c
    signal.signal(signal.SIGINT, handle_child_exit)
    time.sleep(5)
    print(f"child2 finished")
    return "process2"


if __name__ == "__main__":
    child_process1 = Process(target=process1, args=())
    child_process1.start()
    child_process2 = Process(target=process2, args=())
    child_process2.start()
    print(f"main self {os.getpid()}")
    print(f"main parent {os.getppid()}")


    # print(f"main group id {os.getpgid(os.getpid())}")

    def handle_exit(signum, frame):
        child_process1.terminate()
        print("child process terminated")
        sys.exit(0)


    # kill(kill -9不生效)
    signal.signal(signal.SIGTERM, handle_exit)
    # ctrl + c
    signal.signal(signal.SIGINT, handle_exit)

    # time.sleep(10000)
    # 创建队列
    # q = Queue()
    # q.get(timeout="6")
    # print("=====")
    # poller = zmq.Poller()
    # poller.register(child_process.sentinel, zmq.POLLIN)

    print("================")
    print(any([10, 0]))

    fd1 = child_process1.sentinel  # 子进程句柄
    fd2 = child_process2.sentinel  # 子进程句柄

    # 子进程结束，变为可读，这里的可读并不是“有数据”，而是 可以读取到 EOF，该方法阻塞到任意一个进程结束
    # readable, writable, exceptional = select.select([fd1, fd2], [], [])  # rlist为可读事件，类似于io多路复用
    # for fd in readable:
    #     data = os.read(fd, 1024)
    #     print(f"从 fd {fd} 读到数据：", data.decode())

    """
    select.EPOLLIN     # 可读
    select.EPOLLOUT    # 可写
    select.EPOLLERR    # 错误
    select.EPOLLHUP    # 关闭/挂起
    select.EPOLLET     # 边缘触发（Edge Triggered）
    """
    epoll = select.epoll()
    epoll.register(fd1, select.EPOLLIN)
    epoll.register(fd2, select.EPOLLIN)
    while True:
        events = epoll.poll(50)  # 阻塞最多 5 秒
        for fd, event in events:
            print(f"fd is {fd}")
            # if fd == child_process1.sentinel.fileno():
            #     print("Child process finished (epoll detected)")
            # elif fd == child_process2.sentinel:
            #     print("Socket ready to accept")
