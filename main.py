import threading
import time

def collatz_steps(n, M):
    total_time = 0
    total_steps = 0
    for _ in range(M):
        start_time = time.time()
        steps = 0
        while n != 1:
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            steps += 1
        end_time = time.time()
        total_time += end_time - start_time
        total_steps += steps

    return total_time, total_steps

def calculate_average_steps(numbers, num_threads, M):
    start_time = time.time()
    total_time = 0
    total_steps = 0
    lock = threading.Lock()

    def worker(thread_num):
        nonlocal total_time, total_steps
        while True:
            with lock:
                if not numbers:
                    break
                n = numbers.pop()
            time_per_number, steps_per_number = collatz_steps(n, M)
            with lock:
                total_time += time_per_number
                total_steps += steps_per_number

                if 0: #Прінт показників сповільнює процес.
                    print(f"Потік {thread_num + 1} обробив число {n} за {time_per_number:.5f} секунд " f"з {steps_per_number} кроками")
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    return total_steps, end_time - start_time

if __name__ == "__main__":
    N = int(input("Введіть кількість чисел: "))
    num_threads = int(input("Введіть кількість потоків: "))
    M = int(input("Введіть кількість разів обчислити послідовність Коллаца для кожного числа: "))
    #M - змінна для того щоб штучно збільшити час обробки одного числа. Виставляти на 1 якщо більше не треба
    numbers = list(range(1, N + 1))
    total_steps, execution_time = calculate_average_steps(numbers, num_threads, M)
    print(f"Середня кількість кроків: {total_steps/N:.2f}")
    print(f"Час виконання всіх потоків: {execution_time:.5f} секунд")
