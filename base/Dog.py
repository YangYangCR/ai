import zmq
import multiprocessing


class Dog():

    def __init__(self):
        super().__init__()
        print("this is dog")


def data():
    yield 1, 100, 200


def get_user_info():
    yield "Alice", 25, "alice@email.com"


def multi_data():
    yield 1, 2, 3
    yield 4, 5, 6
    yield 7, 8, 9


if __name__ == "__main__":
    dog = Dog()
    data1, data2, data3 = next(data())
    print(f"{data1}, {data2}, {data3}")

    name, age, email = next(get_user_info())
    print(f"{name}, {age}, {email}")  # Alice, 25, alice@email.com

    for item in multi_data():
        print(type(item))
        print(item)

    print(1_000_000 * 256 / 1024 / 1024)

    # ctx = zmq.Context()
    # sync_push = ctx.socket(zmq.PUSH)
    # sync_push.connect(f"tcp://localhost:5555")
    # sync_push.send_string("xxx")
    # print("send success")
    # queue = multiprocessing.Queue()
    # queue.get()
    print(1772778504.774991 - 1772778499.3782356)
