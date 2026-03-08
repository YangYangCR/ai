import multiprocessing

import zmq
import time
import os
from multiprocessing import Process
import argparse

TASK_ADDR = "tcp://127.0.0.1:5555"
ACK_ADDR = "tcp://127.0.0.1:5556"


def producer(msg_count, consumers, msg_size, share_time):
    context = zmq.Context()
    # 发送任务
    push = context.socket(zmq.PUSH)
    push.bind(TASK_ADDR)
    push.setsockopt(zmq.LINGER, 0)
    # 接收ACK
    ack_socket = context.socket(zmq.PULL)
    ack_socket.bind(ACK_ADDR)
    print("[producer] Producer started")
    time.sleep(1)
    start = time.time()
    # 发送任务
    msg = os.urandom(msg_size)
    share_time["start_time"] = start
    for i in range(msg_count):
        push.send_string(msg.decode("latin-1"))
    # poison pill
    for _ in range(consumers + 1000):
        push.send_string("STOP")
    print("[producer] All msg sent")

    end = time.time()
    # 等待 ACK
    ack_count = 0
    while ack_count < msg_count:
        ack_socket.recv()
        ack_count += 1

    duration = end - start
    msg_per_sec = msg_count / duration
    mb_per_sec = (msg_count * msg_size) / (1024 * 1024) / duration
    print(f"[producer] Time: {duration:.4f} s")
    print(f"[producer] Throughput: {msg_per_sec:,.0f} msg/s")
    print(f"[producer] Bandwidth: {mb_per_sec:,.2f} MB/s")

    push.close()
    ack_socket.close()
    context.term()


def worker(worker_id, msg_size, share_time):
    context = zmq.Context()
    pull = context.socket(zmq.PULL)
    pull.connect(TASK_ADDR)
    ack_socket = context.socket(zmq.PUSH)
    ack_socket.connect(ACK_ADDR)
    count = 0
    pid = os.getpid()
    print(f"[consumer{worker_id}]consumer {worker_id} (pid={pid}) started")
    start = None
    while True:
        msg = pull.recv_string()
        if start is None:
            start = time.time()
        if msg == "STOP":
            print(f"Worker {worker_id} exiting, processed {count}")
            break
        # 模拟任务处理
        count += 1
        # time.sleep(0.0001)
        # 发送 ACK
        ack_socket.send(b"")
    end = time.time()
    duration = end - start
    mb_per_sec = (count * msg_size) / (1024 * 1024) / duration
    print(f"[consumer{worker_id}] Received {count} messages")
    print(f"[consumer{worker_id}] Time: {duration:.4f} s")
    print(f"[consumer{worker_id}] Throughput: {count / duration:,.0f} msg/s")
    print(f"[consumer{worker_id}] Bandwidth: {mb_per_sec:,.2f} MB/s")
    pull.close()
    ack_socket.close()
    context.term()


def run_benchmark(msg_size, msg_count, producers, consumers):
    manager = multiprocessing.Manager()
    share_time = manager.dict()
    workers = []
    for i in range(consumers):
        p = Process(target=worker, args=(i, msg_size, share_time))
        p.start()
        workers.append(p)
    prod = Process(target=producer, args=(msg_count, consumers, msg_size, share_time))
    prod.start()
    prod.join()

    for p in workers:
        p.join()

    all_time = time.time() - share_time["start_time"]
    print(f"all time {all_time:.4f} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="zmq 吞吐压测")
    parser.add_argument("--size", type=int, default=256, help="消息大小（字节）")
    parser.add_argument("--count", type=int, default=4_000_000, help="每个生产者发多少条消息")
    parser.add_argument("--producers", type=int, default=1, help="生产者数量")
    parser.add_argument("--consumers", type=int, default=4, help="消费者数量")
    args = parser.parse_args()

    run_benchmark(
        msg_size=args.size,
        msg_count=args.count,
        producers=args.producers,
        consumers=args.consumers,
    )
