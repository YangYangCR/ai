# subscriber.py
import zmq

def main():
    ctx = zmq.Context()

    sub = ctx.socket(zmq.SUB)
    sub.setsockopt_string(zmq.SUBSCRIBE, "Tom")
    sub.connect("tcp://localhost:5558")   # 连接 XPUB

    print("[Subscriber] Waiting for messages...")

    while True:
        msg = sub.recv_string()
        print("[Subscriber] Received:", msg)

if __name__ == "__main__":
    main()