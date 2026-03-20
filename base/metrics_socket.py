# server.py - 服务端
import zmq

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.PULL)  # REPly socket
    socket.bind("tcp://172.23.16.1:12425")  # 绑定到端口

    # 异步接收回复
    while True:
        response = socket.recv_pyobj()
        print(response)
        # if isinstance(response, dict):
        #     print(f"get dict {response}")
        # elif isinstance(response, str):
        #     print(f"get string {response}")
        # else:
        #     print(f"get response {response}")

