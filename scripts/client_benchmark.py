import socket
import ssl
import time
import random
import os
from typing import List

SERVER_HOST = "localhost"
SERVER_PORT = 44446
USE_SSL = False  # Update based on your config
NUM_QUERIES = 50  # Number of queries per file for benchmarking
TEST_FILES = [
    "test_data/10000_lines.txt",
    "test_data/50000_lines.txt",
    "test_data/100000_lines.txt",
    "test_data/250000_lines.txt",
    "test_data/500000_lines.txt",
    "test_data/1000000_lines.txt"
]

def load_lines(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def run_benchmark(test_file: str, reread_on_query: bool):
    print(f"\nBenchmarking file: {test_file} | REREAD_ON_QUERY={reread_on_query}")
    lines = load_lines(test_file)
    queries = random.choices(lines, k=NUM_QUERIES)

    total_time = 0.0
    for query in queries:
        start = time.time()

        try:
            if USE_SSL:
                context = ssl.create_default_context()
                with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
                    with context.wrap_socket(sock, server_hostname=SERVER_HOST) as ssock:
                        ssock.sendall(query.encode() + b'\n')
                        ssock.recv(1024)
            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((SERVER_HOST, SERVER_PORT))
                    sock.sendall(query.encode() + b'\n')
                    sock.recv(1024)

        except Exception as e:
            print(f"[!] Error during benchmark: {e}")
            continue

        end = time.time()
        elapsed = (end - start) * 1000  # in milliseconds
        total_time += elapsed

    avg_time = total_time / NUM_QUERIES
    print(f"Average execution time over {NUM_QUERIES} queries: {avg_time:.2f} ms")

if __name__ == "__main__":
    for test_file in TEST_FILES:
        for reread in [False, True]:
            run_benchmark(test_file, reread_on_query=reread)
