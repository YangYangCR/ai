import asyncio
import time
import threading


# ❌ 同步版本（阻塞）
def sync_demo():
    print("开始")
    time.sleep(2)  # 阻塞
    print("结束")


# async def hello():
#     print("Hello world!")
#     # 异步调用asyncio.sleep(1):
#     await asyncio.sleep(1)
#     print("Hello again!")

async def wget(host):
    print(f"wget {host}...")
    # 连接80端口:
    reader, writer = await asyncio.open_connection(host, 80)
    # 发送HTTP请求:
    header = f"GET / HTTP/1.0\r\nHost: {host}\r\n\r\n"
    writer.write(header.encode("utf-8"))
    await writer.drain()

    # 读取HTTP响应:
    while True:
        line = await reader.readline()
        if line == b"\r\n":
            break
        print("%s header > %s" % (host, line.decode("utf-8").rstrip()))
    # Ignore the body, close the socket
    writer.close()
    await writer.wait_closed()
    print(f"Done {host}.")


async def hello(name):
    # 打印name和当前线程:
    print("Hello %s! (%s)" % (name, threading.current_thread))
    # 异步调用asyncio.sleep(1):
    await asyncio.sleep(1)
    print("Hello %s again! (%s)" % (name, threading.current_thread))
    return name


# async def main():
#     await asyncio.gather(wget("www.sina.com.cn"), wget("www.sohu.com"), wget("www.163.com"))

async def main():
    L = await asyncio.gather(hello("Bob"), hello("Alice"))
    print(L)


if __name__ == "__main__":
    # sync_demo()
    # asyncio.run(async_demo())

    # asyncio.run(hello())
    asyncio.run(hello("Bob"))
    # asyncio.run(main())
