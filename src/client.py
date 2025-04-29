
import socket
import ssl
import logging
import configparser
import os

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config.get("DEFAULT", "host", fallback="127.0.0.1")
PORT = config.getint("DEFAULT", "port", fallback=9999)
BUFFER_SIZE = 4096  # Slightly bigger buffer
ENABLE_SSL = config.getboolean("DEFAULT", "ENABLE_SSL", fallback=False)

SSL_CERT = config.get("DEFAULT", "SSL_CERT", fallback=None)

# Setup logging
os.makedirs("logs", exist_ok=True)  # Ensure log folder exists
logging.basicConfig(
    filename="logs/client.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def send_query(query: str) -> str:
    """Send a query string to the TCP server and return the response."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if ENABLE_SSL:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False  # self-signed cert
            context.verify_mode = ssl.CERT_NONE

            with context.wrap_socket(sock, server_hostname=HOST) as s:
                s.connect((HOST, PORT))
                s.sendall(query.encode("utf-8"))
                response = s.recv(BUFFER_SIZE).decode("utf-8")
        else:
            with sock:
                sock.connect((HOST, PORT))
                sock.sendall(query.encode("utf-8"))
                response = sock.recv(BUFFER_SIZE).decode("utf-8")

        return response.strip()

    except ConnectionRefusedError:
        logging.error("Connection refused. Is the server running?")
        return "Could not connect to server."
    except Exception as e:
        logging.exception("Unexpected error occurred.")
        return f"Error: {str(e)}"

def run_client():
    print(f"Connected to server at {HOST}:{PORT} (SSL Enabled: {ENABLE_SSL})")
    print("Type a string to search, or 'add:<your string>' to add new entries.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Your input > ").strip()
        if user_input.lower() == "exit":
            print("Exiting client.")
            break

        if not user_input:
            print("Please enter a valid non-empty string.")
            continue

        logging.info("Sending query: %s", user_input)
        response = send_query(user_input)
        print(f"Server response: {response}")

if __name__ == "__main__":
    run_client()
