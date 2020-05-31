#!/usr/bin/env python3

import os
import socket
import sys

SOCKET_PATH="/tmp/uniboard.sock"

def start_daemon():
    register = ""

    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(SOCKET_PATH)
    sock.listen(1)

    while True:
        connection, address = sock.accept()
        data = connection.recv(1024)
        message = data.decode("utf-8")
        index = message.find(":")

        if index == -1:
            continue

        command, value = message[:index], message[index+1:]

        if command == "put":
            register = value
        elif command == "get":
            try:
                connection.sendall(("msg:" + register).encode("utf-8"))
                register = ""
            except:
                pass
        elif command == "ping":
            try:
                connection.sendall(str(os.getpid()).encode("utf-8"))
            except:
                pass

        connection.close()

def uniboard_put(value):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    client.send(("put:" + value).encode("utf-8"))

def uniboard_get():
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    client.send("get:".encode("utf-8"))

    data, _ = client.recvfrom(4096)
    decoded = data.decode("utf-8")
    value = decoded[decoded.find(":") + 1:]

    sys.stdout.write(value)

def uniboard_ping():
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(SOCKET_PATH)
        client.send("ping:".encode("utf-8"))

        pid = client.recv(4096).decode("utf-8")
        print(pid)

    except ConnectionRefusedError:
        print("Uniboard not running")
        sys.exit(1)

def main():
    if len(sys.argv) <= 1:
        pass

    command = sys.argv[1]
    if command == "daemon":
        start_daemon()
    elif command == "put":
        uniboard_put(sys.argv[2])
    elif command == "get":
        uniboard_get()
    elif command == "ping":
        uniboard_ping()
    elif command in ["help", "-h", "--help"]:
        pass

if __name__ == "__main__":
    main()
