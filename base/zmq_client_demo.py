# client 客户端
import zmq

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)  # REQuest socket
    # socket.connect("tcp://192.168.153.1:5555")
    socket.connect("ipc:///tmp/8ec0f83b-d25b-4173-9932-19a025e9028a")
    print("connected ...")

    socket.send_string("Hello")  # 发送请求
    print("send data hello...")
    response = socket.recv()  # 接收回复
    print(f"receive : {response}")
