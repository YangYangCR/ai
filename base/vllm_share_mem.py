from vllm.distributed.device_communicators.shm_broadcast import ShmRingBuffer

if __name__ == "__main__":
    shm = ShmRingBuffer(n_reader=2, max_chunks=3, max_chunk_bytes=1024, name=None)
    handle = shm.handle()
    print(handle)
