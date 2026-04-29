class Demo:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __call__(self, parm):
        print("call xxx xxx")


if __name__ == '__main__':
    demo = Demo("Tom", 20)
    print(demo)
    demo("Jack")
