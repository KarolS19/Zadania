import multiprocessing

def factorize_sync(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(number):
    def worker(num, out_q):
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        out_q.put(factors)

    out_q = multiprocessing.Queue()
    processes = []

    # Get number of CPU cores
    num_cores = multiprocessing.cpu_count()

    # Distribute work across cores
    for _ in range(num_cores):
        process = multiprocessing.Process(target=worker, args=(number, out_q))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Collect results from processes
    results = []
    for _ in range(num_cores):
        results.extend(out_q.get())

    return sorted(results)

def factorize(*numbers):
    result = []
    for number in numbers:
        result.append(factorize_sync(number))
    return result

if __name__ == "__main__":
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
