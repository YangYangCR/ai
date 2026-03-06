import zmq
import time


def worker(worker_id):
    context = zmq.Context()
    # 接收任务的套接字
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")
    while True:
        try:
            # 接收任务
            task = receiver.recv_pyobj()
            task_id = task['task_id']
            workload = task['workload']
            print(f"工作者 {worker_id} 处理任务 {task_id}")
            # 模拟工作
            time.sleep(workload / 10.0)
        except KeyboardInterrupt:
            break
    receiver.close()
    context.term()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        worker_id = sys.argv[1]
    else:
        worker_id = "1"
    worker(worker_id)

# 可以启动多个 worker：
# python worker.py 1
# python worker.py 2
# python worker.py 3
