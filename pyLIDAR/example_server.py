"""A minimal test server to simulate LD06 data stream."""

import signal
import socket
import sys
import threading
import time
from types import FrameType
from typing import Optional, Tuple

from read_data import Point, Reading

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

# HOST: str = socket.gethostname()  # local address IP (not external address IP)
HOST: str = "127.0.0.1"
# '0.0.0.0' or '' - conection on all NICs (Network Interface Card),
# '127.0.0.1' or 'localhost' - local conection only (can't connect from remote computer)
# 'Local_IP' - connection only on one NIC which has this IP

PORT: int = 8000  # local port (not external port)


def generate_Reading() -> Reading:
    from random import randint

    start_angle = randint(0, 30_000)
    return Reading(
        radar_speed=randint(1_000, 2_500),
        start_angle=start_angle,
        end_angle=start_angle + 5085,
        timestamp=randint(1_000, 6_000),
        points=[
            Point(
                distance=randint(50, 300),
                angle=start_angle + randint(0, 5_000),
                confidence=randint(100, 220),
            )
            for _ in range(0, 12)
        ],
    )


def convert_chunk(two_ints: int) -> str:
    hex_str = two_ints.to_bytes(2, byteorder="big").hex()
    final_string = hex_str[2:] + hex_str[:2]
    return final_string


def convert_reading_to_hex(data: Reading) -> str:
    radar_str = convert_chunk(data.radar_speed)
    start_str = convert_chunk(data.start_angle)
    end_str = convert_chunk(data.end_angle)
    time_str = convert_chunk(data.timestamp)

    point_list = [
        convert_chunk(each.distance)
        + each.confidence.to_bytes(1, byteorder="big").hex()
        for each in data.points
    ]

    final_str = (
        "54" + radar_str + start_str + "".join(point_list) + end_str + time_str + "1a50"
    )

    return final_str


def handle_client(conn: socket.socket, addr: Tuple[str, str]) -> None:
    print("Entered")
    try:
        while True:

            new_readings = [generate_Reading() for _ in range(0, 4)]
            new_hex = "".join([convert_reading_to_hex(each) for each in new_readings])
            print(new_hex[0:12])
            conn.send(bytes.fromhex(new_hex))
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
    # Derived from
    # https://stackoverflow.com/questions/57925492/how-to-listen-continuously-to-a-socket-for-data-in-python

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
