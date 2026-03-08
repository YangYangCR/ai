import zmq
import time
import os
import multiprocessing as mp
import argparse

from vllm.distributed.device_communicators.shm_broadcast import MessageQueue, Handle


def enqueue_worker(msg_count, msg_size, queue: MessageQueue, consumers: int, share_dict):
    """PUSH 端作为服务端"""
    batch_size = 1024 * 10  # 一次最少发送10K的消息
    print(f"[producer] start")
    msg = os.urandom(msg_size)  # 二进制消息
    start = time.time()
    share_dict["start_time"] = start
    buffer = []
    for i in range(msg_count):
        buffer.append(msg)
        if len(buffer) >= batch_size:
            # 一次写入 batch_size 条消息
            queue.enqueue(buffer)
            buffer = []
    # 写入剩余消息
    if buffer:
        queue.enqueue(buffer)
    for _ in range(consumers):
        queue.enqueue("stop")
    end = time.time()
    duration = end - start
    msg_per_sec = msg_count / duration
    mb_per_sec = (msg_count * msg_size) / (1024 * 1024) / duration
    print(f"[producer] Time: {duration:.4f} s")
    print(f"[producer] Throughput: {msg_per_sec:,.0f} msg/s")
    print(f"[producer] Bandwidth: {mb_per_sec:,.2f} MB/s")


def dequeue_worker(worker_id: int, msg_size: int, handle: Handle, rank: int, share_dict):
    queue = MessageQueue.create_from_handle(handle, rank)
    queue.wait_until_ready()
    print(f"[consumer{worker_id}] dequeue worker started...")
    start = None
    received = 0
    while True:
        msgs = queue.dequeue()  # 如果是批量消息，返回列表
        if isinstance(msgs, list):
            for msg in msgs:
                if msg == "stop":
                    break
                if start is None:
                    start = time.time()
                received += 1
            if "stop" in msgs:
                break
        else:
            if msgs == "stop":
                break
            if start is None:
                start = time.time()
            received += 1
    end = time.time()
    duration = end - start
    mb_per_sec = (received * msg_size) / (1024 * 1024) / duration
    print(f"[consumer{worker_id}] Received {received} messages")
    print(f"[consumer{worker_id}] Time: {duration:.4f} s")
    print(f"[consumer{worker_id}] Throughput: {received / duration:,.0f} msg/s")
    print(f"[consumer{worker_id}] Bandwidth: {mb_per_sec:,.2f} MB/s")


def run_benchmark(msg_size, msg_count, consumers):
    print(f"======== zmq benchmark ========")
    print(f"消息大小: {msg_size} bytes")
    print(f"消息数量: {msg_count} ")
    print(f"消费者数量: {consumers}")
    print("===================================================\n")

    queue = MessageQueue(
        n_reader=consumers,
        n_local_reader=consumers,
        local_reader_ranks=[i for i in range(consumers)],
        max_chunk_bytes=1024 * 1024 * 100,  # 100M chunk大小 多条消息攒到max_chunk_bytes大小，然后通过zmq发送
        max_chunks=10,
    )
    handle = queue.export_handle()

    manager = mp.Manager()
    share_dict = manager.dict()
    # 启动消费者
    consumer_pool = []
    for i in range(consumers):
        p = mp.Process(target=dequeue_worker, args=(i, msg_size, handle, i, share_dict))
        consumer_pool.append(p)
        p.start()
    queue.wait_until_ready()
    time.sleep(5)
    print("All consumers are fully connected")
    # 启动生产者
    p = mp.Process(target=enqueue_worker, args=(msg_count, msg_size, queue, consumers, share_dict))
    p.start()
    for p in consumer_pool:
        p.join()
    all_time = time.time() - share_dict["start_time"]
    print(f"all time {all_time}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="zmq 吞吐压测")
    parser.add_argument("--size", type=int, default=256, help="消息大小（字节）")
    parser.add_argument("--count", type=int, default=1_000_000, help="每个生产者发多少条消息")
    parser.add_argument("--consumers", type=int, default=2, help="消费者数量")
    args = parser.parse_args()

    run_benchmark(
        msg_size=args.size,
        msg_count=args.count,
        consumers=args.consumers,
    )
