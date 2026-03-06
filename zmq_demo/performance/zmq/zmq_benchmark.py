import zmq
import time
import os
import multiprocessing as mp
import argparse
import threading
from zmq.utils.monitor import recv_monitor_message


def monitor_thread(ctx, ready_event, except_consumers, stop_event):
    monitor = ctx.socket(zmq.PAIR)
    monitor.connect("inproc://monitor.push")
    connections = 0
    while True:
        event = recv_monitor_message(monitor)
        if event["event"] == zmq.EVENT_ACCEPTED:
            connections += 1
            print(f"[monitor] consumer connected: {connections}")
            if connections == except_consumers:
                print("[monitor] enough consumers connected")
                time.sleep(3)
                ready_event.set()
        if event["event"] == zmq.EVENT_DISCONNECTED:
            connections -= 1
            print(f"[monitor] consumer disconnected: {connections}")
            if connections == 0:
                print(f"[monitor] all consumer disconnected")
                stop_event.set()
                break


def push_worker(msg_count, msg_size, consumer_count: int, share_time):
    """PUSH 端作为服务端"""
    print(f"[producer] start")
    msg = os.urandom(msg_size)  # 二进制消息
    ctx = zmq.Context()
    push = ctx.socket(zmq.PUSH)
    push.setsockopt(zmq.LINGER, 0)
    push.bind("tcp://*:5557")
    # 开启 monitor
    push.monitor("inproc://monitor.push", zmq.EVENT_ALL)
    ready_event = threading.Event()
    stop_event = threading.Event()
    t = threading.Thread(target=monitor_thread, args=(ctx, ready_event, consumer_count, stop_event))
    t.daemon = True
    t.start()
    print("producer waiting for consumers...")
    # 等待连接数达到要求
    ready_event.wait()

    print(f"[producer] Sending {msg_count} messages ({msg_size} bytes each)...")
    start = time.time()
    print(f"[producer] start {start}")
    share_time["start_time"] = start
    send_count = 0
    msg_count += 100
    while send_count <= msg_count and not stop_event.is_set():
        push.send_string(msg.decode("latin-1"))
        send_count += 1
    # for _ in range(msg_count):
    #     push.send_string(msg.decode("latin-1"))
    # try:
    #     for _ in range(10000):
    #         push.send_string("stop")
    #         msg_count += 1
    # except zmq.Again:
    #     pass
    print(f"[producer] all msg send ...")
    end = time.time()
    print(f"[producer] end {end}")
    duration = end - start
    msg_per_sec = msg_count / duration
    mb_per_sec = (msg_count * msg_size) / (1024 * 1024) / duration
    print(f"[producer] Time: {duration:.4f} s")
    print(f"[producer] Throughput: {msg_per_sec:,.0f} msg/s")
    print(f"[producer] Bandwidth: {mb_per_sec:,.2f} MB/s")


def pull_worker(worker_id: int, msg_count: int, msg_size: int, ready_event, share_time):
    """PULL 端作为客户端，主动连接 PUSH 服务端"""
    ctx = zmq.Context()
    pull = ctx.socket(zmq.PULL)
    pull.connect("tcp://localhost:5557")  # 监听端口
    print(f"[consumer{worker_id}] start")
    start = None
    received = 0
    while received < msg_count:
        try:
            pull.recv_string()
            # print(f"[consumer{worker_id}] Received: ", msg)
            if start is None:
                start = time.time()
            received += 1
            # print("收到消息:", msg)
        except zmq.Again:
            print("超时，没有收到消息")
            break

    end = time.time()
    share_time[f"end_time_{worker_id}"] = end
    duration = end - start
    mb_per_sec = (received * msg_size) / (1024 * 1024) / duration
    print(f"[consumer{worker_id}] Received {received} messages")
    print(f"[consumer{worker_id}] Time: {duration:.4f} s")
    print(f"[consumer{worker_id}] Throughput: {received / duration:,.0f} msg/s")
    print(f"[consumer{worker_id}] Bandwidth: {mb_per_sec:,.2f} MB/s")


def run_benchmark(msg_size, msg_count, producers, consumers):
    total_msgs = msg_count * producers
    print(f"======== zmq benchmark ========")
    print(f"消息大小: {msg_size} bytes")
    print(f"消息数量: {msg_count} per producer (总 {total_msgs})")
    print(f"生产者数量: {producers}")
    print(f"消费者数量: {consumers}")
    print("===================================================\n")

    manager = mp.Manager()
    share_time = manager.dict()
    ready_events = [mp.Event() for _ in range(consumers)]

    # 启动消费者
    consumer_pool = []
    for i in range(consumers):
        p = mp.Process(target=pull_worker, args=(i, msg_count // consumers, msg_size, ready_events[i], share_time))
        consumer_pool.append(p)
        p.start()

    # 等所有消费者 connect 完成
    # for e in ready_events:
    #     e.wait()
    # print("All consumers are fully connected")
    # 启动生产者
    time.sleep(5)
    producer_pool = []
    for _ in range(producers):
        p = mp.Process(target=push_worker, args=(total_msgs, msg_size, consumers, share_time))
        producer_pool.append(p)
        p.start()

    for p in producer_pool:
        p.join()
    for p in consumer_pool:
        p.join()
    print("all task finished")
    max_endtime = time.time() - 24 * 60 * 60
    print(share_time.keys())
    for k in share_time.keys():
        print(f"values is {share_time[k]}")
        if k.startswith("end_time_") and share_time[k] >= max_endtime:
            max_endtime = share_time[k]
    all_time = max_endtime - share_time.get("start_time", None)
    print(f"all spend time: {all_time:.4f} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="zmq 吞吐压测")
    parser.add_argument("--size", type=int, default=256, help="消息大小（字节）")
    parser.add_argument("--count", type=int, default=100000, help="每个生产者发多少条消息")
    parser.add_argument("--producers", type=int, default=1, help="生产者数量")
    parser.add_argument("--consumers", type=int, default=1, help="消费者数量")
    args = parser.parse_args()

    run_benchmark(
        msg_size=args.size,
        msg_count=args.count,
        producers=args.producers,
        consumers=args.consumers,
    )
