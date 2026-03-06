import zmq
import time


def proxy_server():
    context = zmq.Context()
    # 工作者连接到代理
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5560")
    while True:
        try:
            request = socket.recv_string()
            print(f"工作者收到: {request}")
            time.sleep(0.5)
            socket.send_string(f"处理完成: {request}")
        except KeyboardInterrupt:
            break
    socket.close()
    context.term()


if __name__ == "__main__":
    proxy_server()