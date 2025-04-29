# test_benchmark_server.py

import socket

HOST = '135.181.96.160'  # Benchmark server IP
PORT = 44445             # Benchmark server port
BUFFER_SIZE = 1024
SSL = False              #  SSL=False

def test_query(query: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(query.encode('utf-8'))
        response = s.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Server response: {response}")

if __name__ == "__main__":
    search_string = input("Enter string to search: ")
    test_query(search_string)
