Project Overview
Briefly describe what the project does:

This project implements a multithreaded TCP server that securely handles client requests to search for strings in large files. It supports concurrent connections, secure communication using SSL or PSK, configurable runtime behaviors, and optimized file search algorithms. The system is tested, benchmarked, and production-ready with logging and error handling.

2. Features
Multithreaded TCP server for concurrent client connections

SSL and Pre-Shared Key (PSK) authentication support

Efficient string search in large text files

Configurable settings (e.g., file path, REREAD_ON_QUERY flag)

Optimized search algorithms with performance benchmarking

Structured logging (timestamp, client IP, duration, etc.)

Unit-tested with pytest for robust code coverage

Graceful error handling and service shutdown

3. Installation Instructions
List steps to set up the environment:

# Clone the repository
git clone https://github.com/rasheey97-alt/tcp_string_search_project
cd string-search-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

4. 🏁 Running the Server
Update the config.ini file with the correct file path and flags.

To run with SSL:

python3 server.py --ssl
To run with PSK authentication:


python3 server.py --psk
You can also configure this as a systemd service (include  .service file if needed).

5.  Client Instructions
Run client.py to send search queries:


python3 client.py "search_term"
The client will connect to the server, send the string, and receive the count of lines that contain it.

6.  Testing Instructions
Run unit tests using:


pytest
Test coverage includes:

File reading and line searching

Socket communication

Error cases (e.g., missing file, invalid input)

Security scenarios (unauthorized connection)

7.  Benchmarking Report
A complete benchmarking report (benchmark_report.pdf) is included in the repository.

It compares different search strategies:

readlines()

mmap

Generator-based streaming

The fastest method under realistic load was selected for production use.

8. Security Notes
Secure connection supported via SSL or PSK

Buffer overflow protections in place

User input sanitized

Logging includes client IP for traceability

Authentication can be toggled via config

9. Code Quality
Code adheres to PEP8 and PEP20 guidelines

Type hints and detailed docstrings are used

Project follows clean code principles

Easy to extend or integrate with other systems


Running as a Linux Daemon (systemd service)
To run the server as a background service on a Linux machine, follow these steps:

 Step 1: Create a systemd Service File
Create a file called string-search.service in /etc/systemd/system/:


sudo nano /etc/systemd/system/string-search.service
Paste the following content:


[Unit]
Description=Multithreaded String Search Server
After=network.target

[Service]
User=yourusername
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/python3 /path/to/your/project/server.py
Restart=on-failure
Environment="PYTHONUNBUFFERED=1"


WantedBy=multi-user.target
 Replace /path/to/your/project and yourusername with your actual directory and Linux username.

 Step 2: Reload systemd and Enable the Service

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable string-search.service
 Step 3: Start and Manage the Service

sudo systemctl start string-search.service   # Start the service
sudo systemctl status string-search.service  # Check status
sudo systemctl stop string-search.service    # Stop the service
 Step 4: Check Logs (Optional)
You can monitor output logs via journalctl:

journalctl -u string-search.service -f



# tcp_string_search_project
