import zmq

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket.send(b"hello")
    msg = socket.recv()
    print("client receive ", msg)
