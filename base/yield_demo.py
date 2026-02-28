

def show():
    yield 100
    print(10)

if __name__ == "__main__":
    gen = show()
    print(next(gen))
    print(next(gen))