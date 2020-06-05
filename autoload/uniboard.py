#!/usr/bin/env python3

import argparse
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
        elif command == "stop":
            print("Received 'stop'...exiting")
            sys.exit(0)

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

def uniboard_stop():
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(SOCKET_PATH)
        client.send("stop:".encode("utf-8"))

    except ConnectionRefusedError:
        print("Uniboard not running")
        sys.exit(1)

    print("Uniboard daemon stopped")

def main():
    parser = argparse.ArgumentParser(description='A minimalistic clipboard server')
    parser.add_argument('--daemon', action='store_true',
                        help='Run clipboard daemon')
    parser.add_argument('--put', metavar="VALUE",
                        help='Sets the clipboard value')
    parser.add_argument('--get', action='store_true',
                        help='Returns and clears the clipboard value')
    parser.add_argument('--ping', action='store_true',
                        help='Returns pid of currently running daemon')
    parser.add_argument('--stop', action='store_true',
                        help='Stops the currently running daemon')
    args = parser.parse_args()

    if args.daemon:
        start_daemon()
    elif args.put:
        uniboard_put(args.put)
    elif args.get:
        uniboard_get()
    elif args.ping:
        uniboard_ping()
    elif args.stop:
        uniboard_stop()

if __name__ == "__main__":
    main()
