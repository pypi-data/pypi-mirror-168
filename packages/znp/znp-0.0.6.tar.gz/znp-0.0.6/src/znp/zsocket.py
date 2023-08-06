#!/usr/bin/env python3
import os
import signal
import socket
import sys
import time
from threading import Thread


class SocketListener:
    """
    Run a socket listener in the background and listen for x connections
    """

    def __init__(self, server_address, expected_messages=1):
        self.server_address = server_address
        self.expected = expected_messages
        self.recieved = 0
        self.pids = []
        self.pid_dict = {}
        self.setup()
        thread = Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()

    def run(self):
        # Create storage to be used in loop
        pids = []
        pid_dict = {}
        # Create a UDS socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # Bind the socket to the address
        sock.bind(self.server_address)
        # Chmod the socket
        os.chmod(self.server_address, mode=0o600)
        # Listen for incoming connections
        sock.listen(self.expected)
        # Loop until recieved the expected number of connections
        while self.recieved < self.expected:
            # Clean up data for new connection
            path = None
            pid = None
            # Listen for connection
            connection, client_address = sock.accept()
            # Connection found, try receiving info
            try:
                while True:
                    # Get header, should be a pid padded with zeros
                    if not pid:
                        pid = connection.recv(7)
                    # Store temp_data
                    temp_path = connection.recv(1024)
                    if temp_path:
                        # Set data to temp_data if none stored yet
                        if not path:
                            path = temp_path
                        # Else add it to already stored data
                        else:
                            path = path + temp_path
                    # Connection complete store info
                    else:
                        # Decode message
                        pid = pid.decode(encoding="utf-8")
                        pid = str(int(pid))
                        path = path.decode(encoding="utf-8")
                        # self.pids.append(header)
                        pids.append(pid)
                        # self.pid_dict[header] = []
                        pid_dict[pid] = []
                        # self.pid_dict[header].extend([path, f"{pid}: {path}"])
                        pid_dict[pid].extend([path, f"{pid}: {path}"])
                        break
            finally:
                # Clean up the connection
                connection.close()
                self.recieved += 1
        # Finished receiving data, store it
        self.pids = pids
        self.pid_dict = pid_dict

    def setup(self):
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise


def send_to_socket(pid, parent_pid, file_path, server_address):
    """
    Send message to socket.
    The pid is used as the header.
    The file_path is used as the message.
    The server_address is the address to send the message to.
    """
    # Set pid to 0000000 if none given
    if not pid:
        pid = "0000000"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Try connecting
    try:
        sock.connect(server_address)
    except socket.error as msg:
        print(f"Received error: {msg}\nKilling server.", sys.stderr)
        os.kill(parent_pid, signal.SIGKILL)
        return 1
    # Try sending data
    try:
        pid = bytes(str(pid).zfill(7), encoding="utf-8")
        file_path = bytes(str(file_path), encoding="utf-8")
        sock.sendall(pid)
        sock.sendall(file_path)
    finally:
        sock.close()

    return 0
