import zmq
import time
import os


def publisher(topic_count: int):
    context = zmq.Context()
    # 创建 PUB 类型套接字（发布端）
    socket = context.socket(zmq.PUB)
    # 绑定到端口
    socket.bind("tcp://*:5556")
    print("发布者启动，开始发布消息...")
    # 给订阅者一点连接时间
    time.sleep(1)
    # topics = ["sports", "weather", "news"]
    topics = [f"topic{i}" for i in range(1, topic_count + 1)]
    print(topics)
    message_size = 256
    message = os.urandom(message_size)
    message_count = 1_000_000
    message_count_per_topic = message_count // topic_count
    try:
        for topic in topics:
            for _ in range(message_count_per_topic):
                socket.send_string(f"{topic}")
                # print(f"发布 [{topic}]: {message}")

    except KeyboardInterrupt:
        print("发布者关闭")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    publisher(3)
