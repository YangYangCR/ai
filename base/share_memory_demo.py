import time
from multiprocessing import shared_memory

if __name__ == '__main__':
    # 1024字节大小的共享内存，相当于java中 byte[1024]
    shm = shared_memory.SharedMemory(create=True, size=1024)
    # 给自己数组第一位赋值
    shm.buf[0] = 100
    shm.buf[1:] = 100
    print(f"name {shm.name} created")
    time.sleep(10000)