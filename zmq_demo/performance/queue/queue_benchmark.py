#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
multiprocessing.Queue() 吞吐压测工具
"""

import multiprocessing as mp
import time
import os
import argparse
from multiprocessing.managers import DictProxy


def producer_worker(q: mp.Queue, msg_size: int, count: int, consumers: int, share_time: DictProxy):
    """生产者进程"""
    msg = os.urandom(msg_size)
    start = time.time()
    share_time["start_time"] = start
    print(f"producer start {start:.4f} s")
    for _ in range(count):
        q.put(msg)
    end = time.time()
    dt = end - start
    print(f"[producer]Count: {count}")
    print(f"[producer]Time: {dt:.4f} s")
    print(f"[producer]Throughput: {count / dt:,.0f} msg/s")
    print(f"[producer]Bandwidth:   {msg_size * count / (1024 * 1024):,.2f} MB/s\n")
    for _ in range(consumers):
        q.put("stop")
    return end - start


def consumer_worker(q: mp.Queue, msg_size: int, count: int, worker_id: int, share_time: DictProxy):
    """消费者进程"""
    print(f"[consumer{worker_id}]start")
    start = None
    read_count = 0
    while True:
        try:
            msg = q.get()
            if msg == "stop":
                break
            if start is None:
                start = time.time()
            read_count += 1
        except EOFError:
            print(f"[consumer{worker_id}]stop")
    end = time.time()
    duration = end - start
    share_time["end_time"] = end
    print(f"consumer end {end:.4f} s")
    print(f"[consumer{worker_id}]count: {read_count}")
    print(f"[consumer{worker_id}]Time: {duration:.4f} s")
    print(f"[consumer{worker_id}]Throughput: {read_count / duration:,.0f} msg/s")
    print(f"[consumer{worker_id}]Bandwidth: {msg_size * read_count / (1024 * 1024) / duration:,.2f} MB/s\n")
    return end - start


def run_benchmark(msg_size, msg_count, producers, consumers):
    total_msgs = msg_count * producers
    print(f"======== multiprocessing.Queue() benchmark ========")
    print(f"消息大小: {msg_size} bytes")
    print(f"消息数量: {msg_count} per producer (总 {total_msgs})")
    print(f"生产者数量: {producers}")
    print(f"消费者数量: {consumers}")
    print("===================================================\n")

    manager = mp.Manager()
    share_time = manager.dict()
    # 指定创建子进程方式
    ctx = mp.get_context("spawn")
    q = ctx.Queue(maxsize=total_msgs + 1)
    # 启动消费者
    consumer_pool = []
    for i in range(consumers):
        p = mp.Process(target=consumer_worker, args=(q, msg_size, msg_count, i, share_time))
        consumer_pool.append(p)
        p.start()
    time.sleep(0.5)
    # 启动生产者
    producer_pool = []
    for _ in range(producers):
        p = mp.Process(target=producer_worker, args=(q, msg_size, total_msgs, consumers, share_time))
        producer_pool.append(p)
        p.start()
    for p in producer_pool:
        p.join()
    for p in consumer_pool:
        p.join()
    all_time = share_time.get("end_time", None) - share_time.get("start_time", None)
    print(f"all spend time: {all_time:.4f} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="multiprocessing.Queue() 吞吐压测")
    parser.add_argument("--size", type=int, default=256, help="消息大小（字节）")
    parser.add_argument("--count", type=int, default=1000000, help="每个生产者发多少条消息")
    parser.add_argument("--producers", type=int, default=1, help="生产者数量")
    parser.add_argument("--consumers", type=int, default=2, help="消费者数量")
    args = parser.parse_args()

    run_benchmark(
        msg_size=args.size,
        msg_count=args.count,
        producers=args.producers,
        consumers=args.consumers,
    )
