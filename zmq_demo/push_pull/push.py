import zmq
import time
import random


def ventilator():
    context = zmq.Context()
    # 用于发送任务的套接字
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://*:5557")
    time.sleep(1)
    try:
        # 分发 10 个任务
        for i in range(10):
            workload = random.randint(1, 100)
            sender.send_pyobj({
                'task_id': i,
                'workload': workload
            })
            print(f"分发任务 {i}: 工作量 {workload}")


    except KeyboardInterrupt:
        print("分发器关闭")
    finally:
        sender.close()
        context.term()


if __name__ == "__main__":
    ventilator()