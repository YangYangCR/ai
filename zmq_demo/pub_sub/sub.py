import zmq
import time

def subscriber(subscribe_topic):
    context = zmq.Context()
    # 创建 SUB 类型套接字（订阅端）
    socket = context.socket(zmq.SUB)
    # 连接到发布者
    socket.connect("tcp://localhost:5556")
    # 设置订阅主题（可以多个）
    socket.setsockopt_string(zmq.SUBSCRIBE, subscribe_topic)
    print(f"订阅者启动，订阅主题: {subscribe_topic}")
    topic_count = 3
    message_size = 256
    message_count = 1_000_000
    message_count_per_topic = message_count // topic_count
    try:
        start_all = time.time()
        count = 0
        while True:
            # 接收消息
            string = socket.recv_string() # 代码阻塞
            print("receive string:", string)
            # topic, message = string.split(' ', 1)
            # print(f"收到 [{topic}]: {message}")
            count += 1
            #if count >= message_count_per_topic: break
        end_all = time.time()
        dt = end_all - start_all
        throughput_msgs = message_count_per_topic / dt
        throughput_mb = (message_count_per_topic * message_size) / (1024 * 1024) / dt
        print(f"总耗时: {dt:.4f} s")
        print(f"吞吐量: {throughput_msgs:,.0f} msg/s")
        print(f"带宽:   {throughput_mb:,.2f} MB/s\n")
    except KeyboardInterrupt:
        print("订阅者关闭")
    finally:
        socket.close()
        context.term()

# 运行不同的订阅者
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = "topic1"
    subscriber(topic)

# 终端运行：
# python subscriber.py topic1    # 只订阅天气
