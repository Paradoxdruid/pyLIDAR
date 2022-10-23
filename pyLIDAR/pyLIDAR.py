"""Script to read LD06 LIDAR datastream and plot an updating graph of data."""

import time
from types import FrameType
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import serial

import read_data


def convert_reading_to_polar(
    reading: read_data.Reading,
) -> Tuple[List[float], List[int]]:
    """Convert a Reading object into a set of polar coordinates theta and r"""

    num_points: int = len(reading.points)
    start_angle: int = reading.start_angle
    end_angle: int = reading.end_angle
    step_size: int = int(((end_angle - start_angle) / num_points))
    angles: List[int] = list(
        range(
            start_angle,
            end_angle,
            step_size,
        )
    )
    angles = angles[:-1]

    out_angles: List[float] = [
        (each / 100) * 3.141529 / 180 for each in angles
    ]  # convert to radians
    # The division by 100 because angle is given as, i.e., 32457 for 324.57 degrees

    distances: List[int] = [each.distance for each in reading.points]

    return (out_angles, distances)


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

        # print(data)  # print to screen

        # ---------  DO YOUR DATA PROCESSING HERE --------------------

        for each in data:
            new_angles: List[float]
            new_radii: List[int]
            new_angles, new_radii = convert_reading_to_polar(each)
            angles.extend(new_angles)
            radii.extend(new_radii)

        # ---------  DO YOUR GRAPHING AND GRAPH UPDATES HERE ---------

        # print("Plot")
        # print(f"{angles=}")
        # print(f"{radii=}")
        ax.plot(angles, radii)
        ax.grid(True)
        fig.canvas.draw()
        fig.show()
        plt.pause(0.05)  # Note this 50 ms delay to prevent freezes
        time.sleep(1)


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
