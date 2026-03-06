import multiprocessing as mp
from vllm.distributed.device_communicators.shm_broadcast import MessageQueue


def reader_main(handle, rank):
    queue = MessageQueue.create_from_handle(handle, rank)
    queue.wait_until_ready()
    msg = queue.dequeue()
    print(f"reader{rank} received:", msg)


def writer_main():
    queue = MessageQueue(
        n_reader=2,
        n_local_reader=2,
        local_reader_ranks=[0, 1],
        max_chunk_bytes=1024 * 1024,
        max_chunks=10,
    )
    handle = queue.export_handle()
    p1 = mp.Process(target=reader_main, args=(handle, 0))
    p2 = mp.Process(target=reader_main, args=(handle, 1))
    p1.start()
    p2.start()
    queue.wait_until_ready()
    queue.enqueue("Tom")
    print("writer sent Tom")
    p1.join()
    p2.join()


if __name__ == "__main__":
    writer_main()