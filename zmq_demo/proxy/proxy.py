import zmq


def proxy():
    context = zmq.Context()
    # 前端：接收客户端的请求
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5559")
    # 后端：转发给工作者
    backend = context.socket(zmq.DEALER)
    backend.bind("tcp://*:5560")
    print("代理服务器启动，转发端口 5559 -> 5560")
    try:
        # 使用内置代理功能
        zmq.proxy(frontend, backend)
    except KeyboardInterrupt:
        print("代理关闭")
    finally:
        frontend.close()
        backend.close()
        context.term()


if __name__ == "__main__":
    proxy()