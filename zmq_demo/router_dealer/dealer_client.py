import zmq
import msgpack
import pickle

if __name__ == "__main__":
    ctx = zmq.Context()
    socket = ctx.socket(zmq.DEALER)
    socket.setsockopt_string(zmq.IDENTITY, "1")  # 自定义 identity
    socket.connect("tcp://172.23.28.11:15712")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    send_message = {
        "type": "task",
        "request_id": "100",
        "engine_inputs": {
            "pdf_path_list": ["/root/project/github/MinerU/demo/pdfs/demo1.pdf",
                              "/root/project/github/MinerU/demo/pdfs/demo2.pdf"]
        },
        "sampling_params": None
    }
    socket.send_multipart([pickle.dumps(send_message)])
    # socks = dict(poller.poll(200000000))
    # if socket in socks and socks[socket] == zmq.POLLIN:
    #     reply = socket.recv_string()
    #     print(f"Received reply: {reply}")
    # else:
    #     print("Timeout: No reply received within 2 seconds")
