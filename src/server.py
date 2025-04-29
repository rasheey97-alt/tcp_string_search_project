# """
# TCP String Search Server

# This server listens for TCP connections and checks whether a given string
# exists in a predefined file. It includes security hardening, logging,
# and configurable performance behavior.
# """


# import socket
# import ssl
# import configparser
# import logging
# import os
# import sys
# import argparse
# import time

# def daemonize():
#     """Fork the current process into a daemon."""
#     if os.fork() > 0:
#         sys.exit(0)  # Exit parent
#     os.setsid()      # Create new session
#     if os.fork() > 0:
#         sys.exit(0)  # Exit second parent
#     sys.stdout.flush()
#     sys.stderr.flush()
#     with open('/dev/null', 'rb', 0) as f:
#         os.dup2(f.fileno(), sys.stdin.fileno())
#     with open('/dev/null', 'ab', 0) as f:
#         os.dup2(f.fileno(), sys.stdout.fileno())
#         os.dup2(f.fileno(), sys.stderr.fileno())

# # Set up logging
# logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# # Load configuration
# config = configparser.ConfigParser()
# config.read('config.ini')
# cfg = config['DEFAULT']

# DATA_FILE = cfg.get('linuxpath', 'data/200K.txt')
# REREAD_ON_QUERY = cfg.getboolean('REREAD_ON_QUERY', fallback=False)
# ENABLE_SSL = cfg.getboolean('ENABLE_SSL', fallback=False)
# HOST = cfg.get('host', '127.0.0.1')
# PORT = int(cfg.get('port', 9999))

# if HOST == '127.0.0.1' or HOST.lower() == 'localhost':
#     HOST = '0.0.0.0'




# SSL_CERT = cfg.get('SSL_CERT', 'ssl/server.crt')
# SSL_KEY = cfg.get('SSL_KEY', 'ssl/server.key')

# def load_data():
#     try:
#         with open(DATA_FILE, 'r') as f:
#             return [line.strip() for line in f.readlines()]
#     except Exception as e:
#         logging.error(f"Failed to load data: {e}")
#         return []

# data = load_data()

# def handle_client(connstream):
#     global data
#     try:
#         while True:
#             received = connstream.recv(4096).decode().strip()
#             if not received:
#                 break
#             logging.info(f"Received: {received}")
#             if received.startswith('add:'):
#                 new_entry = received[4:].strip()
#                 if new_entry:
#                     with open(DATA_FILE, 'a') as f:
#                         f.write(f"{new_entry}\n")
#                     if not REREAD_ON_QUERY:
#                         data.append(new_entry)
#                     connstream.sendall(b"String added successfully.\n")
#             else:
#                 if REREAD_ON_QUERY:
#                     data = load_data()
#                 results = [entry for entry in data if entry == received]
#                 response = f"Found {len(results)} result(s): {', '.join(results)}\n"
#                 connstream.sendall(response.encode())
#     except Exception as e:
#         logging.error(f"Error handling client: {e}")
#     finally:
#         connstream.shutdown(socket.SHUT_RDWR)
#         connstream.close()

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--daemon', action='store_true', help='Run server as daemon')
#     args = parser.parse_args()

#     if args.daemon:
#         daemonize()

#     context = None
#     if ENABLE_SSL:
#         context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#         context.load_cert_chain(certfile=SSL_CERT, keyfile=SSL_KEY)

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#         server_socket.bind((HOST, PORT))
#         server_socket.listen(5)
#         logging.info(f"Server running at {HOST}:{PORT} (SSL Enabled: {ENABLE_SSL})")
#         print(f"Server running at {HOST}:{PORT} (SSL Enabled: {ENABLE_SSL})")
        
#         while True:
#             client_socket, addr = server_socket.accept()
#             connstream = context.wrap_socket(client_socket, server_side=True) if ENABLE_SSL else client_socket
#             logging.info(f"Connection from {addr}")
#             handle_client(connstream)

# if __name__ == "__main__":
#     main()

import socket
import ssl
import configparser
import logging
import os
import sys
import argparse
import time
import signal  # NEW
from report_generator import generate_pdf_report  # NEW: Adjust if your path/module is different

# Global server socket reference for clean shutdown
server_socket = None

def daemonize():
    """Fork the current process into a daemon."""
    if os.fork() > 0:
        sys.exit(0)
    os.setsid()
    if os.fork() > 0:
        sys.exit(0)
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

# Set up logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
cfg = config['DEFAULT']

DATA_FILE = cfg.get('linuxpath', 'data/200K.txt')
REREAD_ON_QUERY = cfg.getboolean('REREAD_ON_QUERY', fallback=False)
ENABLE_SSL = cfg.getboolean('ENABLE_SSL', fallback=False)
HOST = cfg.get('host', '127.0.0.1')
PORT = int(cfg.get('port', 9999))

if HOST == '127.0.0.1' or HOST.lower() == 'localhost':
    HOST = '0.0.0.0'

SSL_CERT = cfg.get('SSL_CERT', 'ssl/server.crt')
SSL_KEY = cfg.get('SSL_KEY', 'ssl/server.key')

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        return []

data = load_data()

def handle_client(connstream):
    global data
    try:
        while True:
            received = connstream.recv(4096).decode().strip()
            if not received:
                break
            logging.info(f"Received: {received}")
            if received.startswith('add:'):
                new_entry = received[4:].strip()
                if new_entry:
                    with open(DATA_FILE, 'a') as f:
                        f.write(f"{new_entry}\n")
                    if not REREAD_ON_QUERY:
                        data.append(new_entry)
                    connstream.sendall(b"String added successfully.\n")
            else:
                if REREAD_ON_QUERY:
                    data = load_data()
                results = [entry for entry in data if entry == received]
                response = f"Found {len(results)} result(s): {', '.join(results)}\n"
                connstream.sendall(response.encode())
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()

def shutdown_handler(signum, frame):
    logging.info("Shutdown signal received. Generating report and closing server...")
    print("\nShutting down gracefully. Generating PDF report...")
    generate_pdf_report()  # ✅ Trigger report generation
    if server_socket:
        server_socket.close()
    sys.exit(0)

def main():
    global server_socket
    parser = argparse.ArgumentParser()
    parser.add_argument('--daemon', action='store_true', help='Run server as daemon')
    args = parser.parse_args()

    if args.daemon:
        daemonize()

    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    context = None
    if ENABLE_SSL:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=SSL_CERT, keyfile=SSL_KEY)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logging.info(f"Server running at {HOST}:{PORT} (SSL Enabled: {ENABLE_SSL})")
    print(f"Server running at {HOST}:{PORT} (SSL Enabled: {ENABLE_SSL})")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            connstream = context.wrap_socket(client_socket, server_side=True) if ENABLE_SSL else client_socket
            logging.info(f"Connection from {addr}")
            handle_client(connstream)
        except Exception as e:
            logging.error(f"Error accepting connection: {e}")

if __name__ == "__main__":
    main()
