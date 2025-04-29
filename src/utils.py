# utils.py
import time

def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"[TIMER] {func.__name__} executed in {time.time() - start:.4f} seconds.")
        return result
    return wrapper
