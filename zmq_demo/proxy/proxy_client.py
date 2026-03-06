import zmq


def proxy_client():
    context = zmq.Context()
    # 客户端连接到代理
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    for i in range(5):
        socket.send_string(f"请求 {i}")
        reply = socket.recv_string()
        print(f"收到: {reply}")
    socket.close()
    context.term()


if __name__ == "__main__":
    proxy_client()