import zmq

if __name__ == "__main__":
    ctx = zmq.Context()
    socket = ctx.socket(zmq.ROUTER)
    socket.connect("tcp://localhost:5555")
    socket.send_string("Tom")