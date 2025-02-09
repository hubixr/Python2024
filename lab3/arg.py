import time
import numpy as np
import statistics

# Dekorator do zliczania czasu wykonywania funkcji i obliczania statystyk
def performance_tracker(func):
    timings = []

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        timings.append(time.perf_counter() - start_time)
        return result

    wrapper.get_stats = lambda: {
        "count": len(timings),
        "average": statistics.mean(timings) if timings else None,
        "min": min(timings, default=None),
        "max": max(timings, default=None),
        "stdev": statistics.stdev(timings) if len(timings) > 1 else 0.0
    }
    return wrapper

# Przykładowa funkcja testowa
@performance_tracker
def matrix_multiplication(size):
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    return np.dot(A, B)

# Testowanie kodu
if __name__ == "__main__":
    for _ in range(10):
        matrix_multiplication(500)

    stats = matrix_multiplication.get_stats()
    print("Statystyki wykonania funkcji:")
    for key, value in stats.items():
        print(f"{key.capitalize()}: {value}")
