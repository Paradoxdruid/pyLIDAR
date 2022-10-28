"""Script to read LD06 LIDAR datastream and plot an updating graph of data."""

import json
import os
from dataclasses import asdict
from types import FrameType
from typing import List, Optional

import matplotlib.pyplot as plt
import read_data
import serial


def main(ser: serial.Serial, plot: bool = False, save: bool = False) -> None:

    if plot is True:
        # Initialize empty figure
        fig: plt.Figure
        ax: plt.Axes
        fig, ax = plt.subplots(subplot_kw={"projection": "polar"})

    # Initialize empty data lists
    angles: List[float] = []
    radii: List[int] = []

    if save is True:
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fname = f"{timestamp}.json"

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
        if plot is True:
            ax.plot(angles, radii)
            ax.grid(True)
            fig.canvas.draw()
            fig.show()
            plt.pause(0.05)  # Note this 50 ms delay to prevent freezes

        # --------- DO YOUR DATA SAVING HERE    -----------------------
        if save is True:

            if os.path.isfile(fname):
                # File exists, so append JSON object to output file JSON array
                with open(fname, "a+") as outfile:
                    outfile.seek(0, os.SEEK_END)  # seek to end of file
                    outfile.seek(outfile.tell() - 1, os.SEEK_SET)
                    outfile.truncate()  # remove array end brace
                    outfile.write(",")
                    json.dump(asdict(data), outfile)
                    outfile.write("]")  # close array
            else:
                # Create empty JSON array
                with open(fname, "w") as outfile:
                    array = []
                    array.append(asdict(data))
                    json.dump(array, outfile)


# Code that runs when file is directly executed, i.e.: `python pyLIDAR.py -p COM4 -s`
if __name__ == "__main__":

    # Use signal handling to break infinite loops
    import signal
    import sys

    def signal_handler(signal: int, frame: Optional[FrameType]) -> None:
        print("\nprogram exiting gracefully")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Set up argument parsing
    import argparse

    parser = argparse.ArgumentParser(description="Collect LIDAR data")
    parser.add_argument("-p", "--port", required=True, help="serial port")
    parser.add_argument("-g", "--graph", action="store_true", help="graph data")
    parser.add_argument("-s", "--save", action="store_true", help="save data")

    args = parser.parse_args()

    port: str = args.port
    plot: bool = args.graph
    save: bool = args.save

    print("Starting LIDAR data collection")

    if port == "test":  # Use local server for testing
        with serial.serial_for_url("socket://127.0.0.1:8000", timeout=1) as ser:
            print("Entered")
            main(ser, plot, save)
            print("Exited")
    else:
        # Open serial port connection to LD06 LIDAR
        with serial.Serial(port, 230400, timeout=1) as ser:
            print("Entered")
            main(ser, plot, save)
            print("Exited")
