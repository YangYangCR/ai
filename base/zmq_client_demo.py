# client 客户端
import zmq

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)  # REQuest socket
    socket.connect("tcp://127.0.0.1:5555")
    # socket.connect("ipc:///tmp/8ec0f83b-d25b-4173-9932-19a025e9028a")
    print("connected ...")

    socket.send_pyobj("Hello")  # 发送请求
    print("send data hello...")
    socket.send_pyobj({"key1": "value1"})  # 发送请求
    print("send data key value...")



