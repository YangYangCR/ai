from concurrent.futures import ThreadPoolExecutor

def task(n):
    return n * 2


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(task, 10)
        result = future.result()
        print(result)

        results = list(executor.map(task, range(10)))
        print(results)



