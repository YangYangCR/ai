import zmq
import multiprocessing as mp
import time
import argparse


# ----------------- Publisher -----------------
def pub_worker(msg_count, msg_size, topics, sync_port, subscriber_count):
    ctx = zmq.Context()
    pub = ctx.socket(zmq.PUB)
    pub.bind("tcp://*:5557")

    # 等待所有 SUB 同步
    sync_pull = ctx.socket(zmq.PULL)
    sync_pull.bind(f"tcp://*:{sync_port}")
    print("[producer] Waiting for subscribers to be ready...")
    for _ in range(subscriber_count):
        sync_pull.recv_string()
    print("[producer] All subscribers ready. Sending messages...")

    # 再 sleep 确保 socket 建立
    time.sleep(0.2)

    msg_count_per_topic = msg_count // len(topics)
    payload = b"x" * msg_size
    start = time.time()
    for topic in topics:
        for _ in range(msg_count_per_topic):
            pub.send_multipart([topic.encode(), payload])
        pub.send_multipart([topic.encode(), b"stop"])
    end = time.time()
    print(f"[Publisher] Done. Time={end - start:.4f}s")
    duration = end - start
    msg_per_sec = msg_count / duration
    mb_per_sec = (msg_count * msg_size) / (1024 * 1024) / duration
    print(f"[producer] Time: {duration:.4f} s")
    print(f"[producer] Throughput: {msg_per_sec:,.0f} msg/s")
    print(f"[producer] Bandwidth: {mb_per_sec:,.2f} MB/s")


# ----------------- Subscriber -----------------
def sub_worker(topic, sync_port):
    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.connect("tcp://localhost:5557")
    sub.setsockopt_string(zmq.SUBSCRIBE, topic)
    print(f"[consumer-{topic}] subscribing to topic {topic}")
    # SYNC: 通知 publisher 已经订阅完成
    sync_push = ctx.socket(zmq.PUSH)
    sync_push.connect(f"tcp://localhost:{sync_port}")
    # 等待建立socket连接
    time.sleep(2)
    sync_push.send_string("READY")

    received = 0
    sub.setsockopt(zmq.RCVTIMEO, 1000)
    start = None
    while True:
        try:
            t, msg = sub.recv_multipart()
            if msg == b"stop":
                # print(f"[Subscriber-{topic}] Received stop message")
                break
            # 从接收到第一条消息开始计时
            if start is None:
                start = time.time()
            received += 1
            # 队列中接收不到消息会触发此异常，在subscriber启动，但是publisher还没有发送消息时，会触发
        except zmq.Again:
            # print(f"[consumer-{topic}] timeout")
            # break
            pass
    # 如果根本没收到任何消息，可以设置 duration = 0
    end = time.time() if start else start
    duration = (end - start) if start else 0
    print(f"[consumer {topic}] Received {received} messages")
    print(f"[consumer {topic}] Time: {duration:.4f} s")
    print(f"[consumer {topic}] Throughput: {received / duration if duration > 0 else 0:,.0f} msg/s")


# ----------------- Runner -----------------
def run_benchmark(msg_size, msg_count, producers, consumers):
    topics = [f"topic{i}" for i in range(consumers)]
    subscriber_count = len(topics)
    sync_port = 5560

    subs = []
    for topic in topics:
        p = mp.Process(target=sub_worker, args=(topic, sync_port))
        subs.append(p)
        p.start()

    # 启动 publisher
    pub = mp.Process(target=pub_worker, args=(msg_count, msg_size, topics, sync_port, subscriber_count))
    pub.start()

    pub.join()
    for s in subs:
        s.join()


# ----------------- Main -----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="topic benchmark")
    parser.add_argument("--size", type=int, default=256, help="Message size in bytes")
    parser.add_argument("--count", type=int, default=100000, help="Messages per publisher")
    parser.add_argument("--producers", type=int, default=1, help="Number of publishers")
    parser.add_argument("--consumers", type=int, default=4, help="Number of subscribers / topics")
    args = parser.parse_args()

    run_benchmark(
        msg_size=args.size,
        msg_count=args.count,
        producers=args.producers,
        consumers=args.consumers
    )
