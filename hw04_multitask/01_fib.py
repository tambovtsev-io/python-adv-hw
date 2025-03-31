import multiprocessing
import threading
import time
from pathlib import Path


def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def run_synchronous(n: int, times: int) -> float:
    start_time = time.time()

    for i in range(times):
        fib_res = fib(n)

    end_time = time.time()
    return end_time - start_time


def run_threaded(n: int, times: int) -> float:
    threads = []
    start_time = time.time()

    for i in range(times):
        thread = threading.Thread(target=fib, args=(n,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    return end_time - start_time


def run_multiprocess(n: int, times: int) -> float:
    processes = []
    start_time = time.time()

    for i in range(times):
        process = multiprocessing.Process(target=fib, args=(n,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    return end_time - start_time


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run Fibonacci calculation methods")
    parser.add_argument(
        "-n", type=int, default=32, help="Number of Fibonacci numbers to calculate"
    )
    parser.add_argument(
        "--times", type=int, default=10, help="Number of parallel executions"
    )
    args = parser.parse_args()

    n = args.n
    times = args.times

    time_sync = run_synchronous(n, times)
    time_thread = run_threaded(n, times)
    time_process = run_multiprocess(n, times)

    artifacts_dir = Path("artifacts") / "01_fib"
    artifacts_dir.mkdir(exist_ok=True)
    artifacts_file = artifacts_dir / "01_fibonacci_comparison.txt"
    with open(artifacts_file, "w") as artifacts_file:
        artifacts_file.write(
            f"Comparison of Multiprocessing Methods (n={n}, runs={times}):\n"
        )
        artifacts_file.write("-" * 60 + "\n")
        artifacts_file.write(f"Synchronous execution time: {time_sync:.3g} seconds\n")
        artifacts_file.write(f"Threaded execution time: {time_thread:.3g} seconds\n")
        artifacts_file.write(
            f"Multiprocess execution time: {time_process:.3g} seconds\n"
        )


if __name__ == "__main__":
    main()
