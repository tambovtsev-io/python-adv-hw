import concurrent.futures
import math
import time
from functools import partial
from multiprocessing import cpu_count
from operator import itemgetter
from pathlib import Path
from typing import Any, Callable, Dict, List

import matplotlib.pyplot as plt
import pandas as pd


def partial_integrate(
    start_idx: int,
    end_idx: int,
    f: Callable[[float], float],
    a: float,
    step: float,
) -> float:
    acc = 0.0
    for i in range(start_idx, end_idx):
        acc += f(a + i * step) * step
    return acc


def integrate(
    f: Callable[[float], float],
    a: float,
    b: float,
    n_iter: int = 10000000,
) -> float:
    step = (b - a) / n_iter
    start_idx = 0
    end_idx = n_iter
    return partial_integrate(start_idx, end_idx, f, a, step)


def integrate_parallel(
    f: Callable[[float], float],
    a: float,
    b: float,
    n_jobs: int = 1,
    n_iter: int = 10000000,
    executor_class: Any = concurrent.futures.ThreadPoolExecutor,
) -> float:

    if n_jobs == 1:
        return integrate(f, a, b, n_iter=n_iter)

    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs

    # Prepare chunks for parallel processing
    chunks: List[Dict[str, Any]] = []
    partial_integrate_func = partial(partial_integrate, f=f, a=a, step=step)
    for i in range(n_jobs):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < n_jobs - 1 else n_iter
        chunks.append(dict(start_idx=start_idx, end_idx=end_idx))

    # Execute in parallel
    with executor_class(max_workers=n_jobs) as executor:
        results = executor.map(
            partial_integrate_func,
            map(itemgetter("start_idx"), chunks),
            map(itemgetter("end_idx"), chunks),
        )

    return sum(results)


def compare_execution_times(f: Callable[[float], float] = math.cos):
    cpu_num = cpu_count()
    n_jobs_range = range(1, cpu_num * 2 + 1)
    results = []

    for n_jobs in n_jobs_range:
        # Thread execution
        start_time = time.time()
        result_thread = integrate_parallel(
            f=f,
            a=0,
            b=math.pi / 2,
            n_jobs=n_jobs,
            executor_class=concurrent.futures.ThreadPoolExecutor,
        )
        thread_time = time.time() - start_time

        # Process execution
        start_time = time.time()
        result_process = integrate_parallel(
            f=f,
            a=0,
            b=math.pi / 2,
            n_jobs=n_jobs,
            executor_class=concurrent.futures.ProcessPoolExecutor,
        )
        process_time = time.time() - start_time

        results.append(
            {"n_jobs": n_jobs, "thread_time": thread_time, "process_time": process_time}
        )

        print(f"n_jobs={n_jobs}:")
        print(
            f"Thread time: {thread_time:.4f}s, integration result: {result_thread:.4f}"
        )
        print(
            f"Process time: {process_time:.4f}s, integration result: {result_process:.4f}"
        )
        print("---")

    return pd.DataFrame(results)


if __name__ == "__main__":
    artifacts_dir = Path("artifacts") / "02_integrate"
    artifacts_dir.mkdir(exist_ok=True)

    df = compare_execution_times()
    df.to_csv(artifacts_dir / "execution_comparison.csv", index=False)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(df["n_jobs"], df["thread_time"], "b-", label="ThreadPoolExecutor")
    plt.plot(df["n_jobs"], df["process_time"], "r-", label="ProcessPoolExecutor")
    plt.xlabel("Number of workers (n_jobs)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Execution Time Comparison: Thread vs Process")
    plt.legend()
    plt.grid(True)
    plt.savefig(artifacts_dir / "execution_comparison.png")
    plt.close()
