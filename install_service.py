import sys
import win32serviceutil
import win32service
import win32event
import win32api
import servicemanager
import os
import time
import subprocess

class TcpService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TcpStringSearchService"  # Name of the service
    _svc_display_name_ = "TCP String Search Service"  # Display name for the service
    _svc_description_ = "This service handles string search requests via TCP connection."  # Description

    def __init__(self, args):
        super(TcpService, self).__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.start_server()

    def start_server(self):
        # This is where the TCP server code goes.
        # You should adapt your TCP server code here.
        # Example: subprocess.call(['python', 'src/server.py'])  # Run the server script.
        
        while True:
            try:
                # The code for your TCP server
                subprocess.call(['python', 'src/server.py'])  # Adjust the path as needed
                time.sleep(1)
            except Exception as e:
                print(f"Error in server: {e}")
                time.sleep(5)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(TcpService)
