# File: script/benchmark_search.py

import time

SEARCH_TERM = "some_query_string\n"
FILE_PATH = "data/200k.txt"

def search_with_readlines():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return SEARCH_TERM in f.readlines()

def search_with_loop():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line == SEARCH_TERM:
                return True
    return False

def search_with_set():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return SEARCH_TERM in set(f)

def benchmark(method):
    start = time.time()
    found = method()
    end = time.time()
    print(f"{method.__name__:<25} | Found: {found} | Time: {round((end - start)*1000, 4)} ms")

# Run all benchmarks
if __name__ == "__main__":
    for method in [search_with_readlines, search_with_loop, search_with_set]:
        benchmark(method)
