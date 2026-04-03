import zmq

if __name__ == "__main__":
    ctx = zmq.Context()

    # 创建两个 PULL socket
    socket1 = ctx.socket(zmq.DEALER)
    socket1.connect("tcp://127.0.0.1:5555")
    socket1.setsockopt(zmq.IDENTITY, b"1")

    socket2 = ctx.socket(zmq.DEALER)
    socket2.connect("tcp://127.0.0.1:5556")
    socket2.setsockopt(zmq.IDENTITY, b"2")

    # 创建 Poller
    poller = zmq.Poller()

    # 注册 socket，监听可读事件
    poller.register(socket1, zmq.POLLIN)
    poller.register(socket2, zmq.POLLIN)

    while True:
        # timeout=1000ms
        events = dict(poller.poll(timeout=10000000))

        if socket1 in events:
            msg = socket1.recv()
            print("socket1 msg:", msg)

        if socket2 in events:
            msg = socket2.recv()
            print("socket2 msg:", msg)
