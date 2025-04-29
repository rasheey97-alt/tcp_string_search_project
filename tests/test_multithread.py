import socket
import time
from concurrent.futures import ThreadPoolExecutor

HOST = "127.0.0.1"
PORT = 9999
BUFFER_SIZE = 1024


def send_query(i):
    try:
        start = time.time()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"test\n")
            response = s.recv(BUFFER_SIZE).decode().strip()
        end = time.time()
        print(f"[Client {i}] Response: {response} | Time: {round((end - start)*1000, 2)} ms")
    except Exception as e:
        print(f"[Client {i}] Error: {e}")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(send_query, range(50))