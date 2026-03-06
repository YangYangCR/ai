import zmq
import threading
from zmq.utils.monitor import recv_monitor_message

EXPECTED_CONSUMERS = 1
MSG_COUNT = 100000


def monitor_thread(ctx, ready_event):
    monitor = ctx.socket(zmq.PAIR)
    monitor.connect("inproc://monitor.push")
    connections = 0
    while True:
        event = recv_monitor_message(monitor)
        if event["event"] == zmq.EVENT_ACCEPTED:
            connections += 1
            print(f"[monitor] consumer connected: {connections}")
            if connections >= EXPECTED_CONSUMERS:
                print("✔ enough consumers connected")
                ready_event.set()


def main():
    ctx = zmq.Context()
    push = ctx.socket(zmq.PUSH)
    push.bind("tcp://*:5557")
    # 开启 monitor
    push.monitor("inproc://monitor.push", zmq.EVENT_ALL)
    ready_event = threading.Event()
    t = threading.Thread(target=monitor_thread, args=(ctx, ready_event))
    t.daemon = True
    t.start()

    print("producer waiting for consumers...")
    ready_event.wait()
    print("producer start sending")
    for i in range(MSG_COUNT):
        push.send_string(f"msg-{i}")
    for _ in range(EXPECTED_CONSUMERS):
        push.send_string("STOP")
    print("producer finished")


if __name__ == "__main__":
    main()