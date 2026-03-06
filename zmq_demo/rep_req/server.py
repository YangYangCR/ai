import zmq

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        msg = socket.recv()
        print("receive msg:", msg)
        socket.send(msg)
