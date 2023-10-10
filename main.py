import threading
import time


def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def average_collatz_steps(N, num_threads):
    numbers = list(range(1, N + 1))
    chunk_size = len(numbers) // num_threads
    results = []

    def compute_range(start, end):
        local_sum = sum(collatz_steps(num) for num in numbers[start:end])
        results.append(local_sum)

    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(numbers)
        thread = threading.Thread(target=compute_range, args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_steps = sum(results)
    average = total_steps / N
    return average

if __name__ == "__main__":
    N = int(input("Введіть кількість чисел: "))
    num_threads = int(input("Введіть кількість потоків: "))

    start_time = time.time()
    average = average_collatz_steps(N, num_threads)
    end_time = time.time()

    print(f"Середня кількість кроків для чисел від 1 до {N}: {average}")
    print(f"Час виконання:  {end_time - start_time}")
