import zmq
import time
import multiprocessing as mp


# ---------------- ROUTER Server ----------------
def router_server(bind_addr="tcp://*:5555"):
    ctx = zmq.Context()
    router = ctx.socket(zmq.ROUTER)
    router.bind(bind_addr)
    print("[ROUTER] Server started...")

    while True:
        try:
            # ROUTER 接收三段消息: [identity][empty][payload]
            identity, empty, msg = router.recv_multipart()
            print(f"[ROUTER] Received from {identity.decode()}: {msg.decode()}")

            # 回复客户端
            reply = f"ACK:{msg.decode()}".encode()
            router.send_multipart([identity, b"", reply])
        except KeyboardInterrupt:
            print("[ROUTER] Server stopped.")
            break


# ---------------- DEALER Client ----------------
def dealer_client(client_id, connect_addr="tcp://localhost:5555", msg_count=1, delay=1.0):
    ctx = zmq.Context()
    dealer = ctx.socket(zmq.DEALER)
    dealer.setsockopt_string(zmq.IDENTITY, client_id)  # 自定义 identity
    dealer.connect(connect_addr)
    print(f"[DEALER-{client_id}] Connected to server")

    for i in range(msg_count):
        msg = f"msg-{i}".encode()
        dealer.send_multipart([b"", msg])
        print(f"[DEALER-{client_id}] Sent: {msg.decode()}")

        # 接收服务器回复
        empty, msg = dealer.recv_multipart()
        print(f"[DEALER-{client_id}] Received: {msg.decode()}")
        time.sleep(delay)


# ---------------- Main ----------------
if __name__ == "__main__":
    # 启动 ROUTER 服务器
    server_process = mp.Process(target=router_server)
    server_process.start()

    # 启动多个 DEALER 客户端
    clients = []
    client_ids = ["Alice", "Bob", "Charlie"]
    for cid in client_ids:
        p = mp.Process(target=dealer_client, args=(cid,))
        clients.append(p)
        p.start()

    # 等待客户端完成
    for p in clients:
        p.join()

    # 停止服务器
    server_process.terminate()
    server_process.join()
