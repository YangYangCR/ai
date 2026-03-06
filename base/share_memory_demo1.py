import time
from multiprocessing import shared_memory

if __name__ == '__main__':
    shm = shared_memory.SharedMemory(name="wnsm_2ca2ac4e")
    print(shm.buf[0])
