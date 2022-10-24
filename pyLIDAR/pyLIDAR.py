"""Script to read LD06 LIDAR datastream and plot an updating graph of data."""

from types import FrameType
from typing import List, Optional

import matplotlib.pyplot as plt
import serial

import read_data


def main(ser: serial.Serial) -> None:

    # Initialize empty figure
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})

    # Initialize empty data lists
    angles: List[float] = []
    radii: List[int] = []

    while True:

        raw_byte: bytes = ser.read(1)  # read one byte
        if not raw_byte[0:1] == b"T":  # If that byte isn't a start character,
            continue  # repeat while loop, don't execute the code below

        raw_bytes: bytes = ser.read(46)  # read the next 46 bytes

        data: read_data.Reading = read_data.read_data(b"T" + raw_bytes)

        # ---------  DO YOUR DATA PROCESSING HERE --------------------

        new_angles: List[float] = [
            (point.angle / 100) * 3.141529 / 180 for point in data.points
        ]  # convert to radians
        new_radii: List[int] = [point.distance for point in data.points]
        angles.extend(new_angles)
        radii.extend(new_radii)

        # ---------  DO YOUR GRAPHING AND GRAPH UPDATES HERE ---------

        ax.plot(angles, radii)
        ax.grid(True)
        fig.canvas.draw()
        fig.show()
        plt.pause(0.05)  # Note this 50 ms delay to prevent freezes


# Code that runs when file is directly executed, i.e.: `python serial_LD.py`
if __name__ == "__main__":

    # Use signal handling to break infinite loops
    import signal
    import sys

    def signal_handler(signal: int, frame: Optional[FrameType]) -> None:
        print("\nprogram exiting gracefully")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("Starting LIDAR data collection")
    try:
        port: str = sys.argv[1]
    except IndexError:
        port = "COM4"  # Default port on Windows

    if port == "test":  # Use local server for testing
        import socket

        with serial.serial_for_url(
            f"socket://{socket.gethostname()}:8000", timeout=1
        ) as ser:
            print("Entered")
            main(ser)
            print("Exited")
    else:
        # Open serial port connection to LD06 LIDAR
        with serial.Serial(port, 230400, timeout=1) as ser:
            print("Entered")
            main(ser)
            print("Exited")
