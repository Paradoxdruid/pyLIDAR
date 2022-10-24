"""A minimal test server to simulate LD06 data stream."""

# Derived from
# https://stackoverflow.com/questions/57925492/how-to-listen-continuously-to-a-socket-for-data-in-python

import signal
import socket
import sys
import threading
import time
from types import FrameType
from typing import Optional, Tuple

SAMPLE: bytes = bytes.fromhex(
    (
        "54 2C 68 08 AB 7E E0 00 E4 DC 00 E2 D9 00 E5 D5 00 E3 D3 00 E4 D0 00 E9 CD 00"
        "E4 CA 00 E2 C7 00 E9 C5 00 E5 C2 00 E5 C0 00 E5 BE 82 3A 1A 50 54 2C 68 08 AB"
        "7E E0 00 E4 DC 00 E2 D9 00 E5 D5 00 E3 D3 00 E4 D0 00 E9 CD 00 E4 CA 00 E2 C7"
        "00 E9 C5 00 E5 C2 00 E5 C0 00 E5 BE 82 3A 1A 50 54 2C 68 08 AB 7E E0 00 E4 DC"
        "00 E2 D9 00 E5 D5 00 E3 D3 00 E4 D0 00 E9 CD 00 E4 CA 00 E2 C7 00 E9 C5 00 E5"
        "C2 00 E5 C0 00 E5 BE 82 3A 1A 50 54 2C 68 08 AB 7E E0 00 E4 DC 00 E2 D9 00 E5"
        "D5 00 E3 D3 00 E4 D0 00 E9 CD 00 E4 CA 00 E2 C7 00 E9 C5 00 E5 C2 00 E5 C0 00"
        "E5 BE 82 3A 1A 50 54 2C 68 08 AB 7E E0 00 E4 DC 00 E2 D9 00 E5 D5 00 E3 D3 00"
        "E4 D0 00 E9 CD 00 E4 CA 00 E2 C7 00 E9 C5 00 E5 C2 00 E5 C0 00 E5 BE 82 3A 1A"
        "50 54 2C 68 08 AB 7E E0 00 E4 DC 00 E2 D9 00 E5 D5 00 E3 D3 00 E4 D0 00 E9 CD"
        "00 E4 CA 00 E2 C7 00 E9 C5 00 E5 C2 00 E5 C0 00 E5 BE 82 3A 1A 50 54 2C 68 08"
        "AB 7E E0 00 E4 DC 00 E2 D9 00 E5 D5 00 E3 D3 00 E4 D0 00 E9 CD 00 E4 CA 00 E2"
        "C7 00 E9 C5 00 E5 C2 00 E5 C0 00 E5 BE 82 3A 1A 50 54 2C 68 08 AB 7E E0 00 E4"
        "DC 00 E2 D9 00 E5 D5 00 E3 D3 00 E4 D0 00 E9 CD 00 E4 CA 00 E2 C7 00 E9 C5 00"
        "E5 C2 00 E5 C0 00 E5 BE 82 3A 1A 50"
    )
)

HOST: str = socket.gethostname()  # local address IP (not external address IP)
# '0.0.0.0' or '' - conection on all NICs (Network Interface Card),
# '127.0.0.1' or 'localhost' - local conection only (can't connect from remote computer)
# 'Local_IP' - connection only on one NIC which has this IP

PORT: int = 8000  # local port (not external port)


def handle_client(conn: socket.socket, addr: Tuple[str, str]) -> None:
    print("Entered")
    # _ = conn.recv(1024)
    # print("Entered and received")
    try:
        # print("Trying")
        while True:
            conn.send(SAMPLE)
            # print("Sent")
            time.sleep(1)
    except BrokenPipeError:
        print("[DEBUG] addr:", addr, "Connection closed by client?")
    except Exception as ex:
        print(
            "[DEBUG] addr:",
            addr,
            "Exception:",
            ex,
        )
    finally:
        conn.close()


def signal_handler(signal: int, frame: Optional[FrameType]) -> None:
    print("\nprogram exiting gracefully")
    sys.exit(0)


# Use signal handling to break infinite loops
signal.signal(signal.SIGINT, signal_handler)

try:
    # --- create socket ---

    print("[DEBUG] create socket")

    s: socket.socket = socket.socket()
    # default value is (socket.AF_INET, socket.SOCK_STREAM)

    # --- options ---

    # solution for "[Error 89] Address already in use". Use before bind()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # --- assign socket to local IP (local NIC) ---

    print("[DEBUG] bind:", (HOST, PORT))

    s.bind((HOST, PORT))  # one tuple (HOST, PORT), not two arguments

    # --- set size of queue ---

    print("[DEBUG] listen")

    s.listen(1)  # number of clients waiting in queue for "accept".
    # If queue is full then client can't connect.

    while True:
        # --- accept client ---

        # accept client and create new socket `conn` (with different port)
        # for this client only
        # and server will can use `s` to accept other clients
        # (if you will use threading)

        print("[DEBUG] accept ... waiting")

        conn: socket.socket
        addr: Tuple[str, str]
        conn, addr = s.accept()  # socket, address

        print("[DEBUG] addr:", addr)

        t: threading.Thread = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

        # all_threads.append(t)

except Exception as ex:
    print(ex)
finally:
    # --- close socket ---

    print("[DEBUG] close socket")

    s.close()
