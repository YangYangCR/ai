# broker.py
import zmq

def main():
    ctx = zmq.Context()

    # XSUB 接收 publishers
    frontend = ctx.socket(zmq.XSUB)
    frontend.bind("tcp://*:5557")

    # XPUB 连接 subscribers
    backend = ctx.socket(zmq.XPUB)
    backend.bind("tcp://*:5558")

    print("[Broker] XSUB ↔ XPUB proxy running...")

    zmq.proxy(frontend, backend)   # 阻塞，正式代理开始

if __name__ == "__main__":
    main()