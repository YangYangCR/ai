# server.py - 服务端
import zmq

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)  # REPly socket
    socket.bind("ipc:///tmp/8ec0f83b-d25b-4173-9932-19a025e9028a")  # 绑定到端口

    # 异步接收回复
    while True:
        try:
            response = socket.recv(flags=zmq.NOBLOCK)
            print(f"收到: {response}")
        except zmq.Again:
            # 没有消息时继续发送或做其他事
            # print("do nothing ...")
            pass
