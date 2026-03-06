import zmq

if __name__ == '__main__':
    ctx = zmq.Context()
    pull = ctx.socket(zmq.PULL)
    pull.connect("tcp://localhost:5557")
    print("consumer started")
    while True:
        msg = pull.recv_string()
        if msg == "STOP":
            print("consumer stop")
            break
        print("recv:", msg)
