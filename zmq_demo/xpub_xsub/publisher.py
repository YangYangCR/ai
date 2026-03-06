# publisher.py
import zmq
import time

def main():
    ctx = zmq.Context()

    pub = ctx.socket(zmq.PUB)
    pub.connect("tcp://localhost:5557")   # 连接到 XSUB

    print("[Publisher] Start sending")

    # 很关键：给 SUB 留时间完成订阅，否则前几条消息会丢！
    time.sleep(0.5)

    for i in range(10):
        msg = f"Tom {i}"
        pub.send_string(msg)
        print("[Publisher] Sent:", msg)
        time.sleep(0.2)

    for i in range(10):
        msg = f"Jerry {i}"
        pub.send_string(msg)
        print("[Publisher] Sent:", msg)
        time.sleep(0.2)

    print("[Publisher] Done.")

if __name__ == "__main__":
    main()