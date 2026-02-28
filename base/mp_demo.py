from multiprocessing import Process, Queue
import time
import random


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


if __name__ == "__main__":
    # 创建队列
    q = Queue()

    # 创建进程
    p1 = Process(target=producer, args=(q, "P1"))
    p2 = Process(target=producer, args=(q, "P2"))
    c1 = Process(target=consumer, args=(q, "C1"))
    c2 = Process(target=consumer, args=(q, "C2"))

    # 启动进程
    p1.start()
    p2.start()
    c1.start()
    c2.start()

    # 等待生产者结束
    p1.join()
    p2.join()

    # 发送结束信号给消费者（每个消费者都需要一个结束信号）
    q.put(None)
    q.put(None)

    # 等待消费者结束
    c1.join()
    c2.join()

    print("所有进程执行完毕")
    print(3)

