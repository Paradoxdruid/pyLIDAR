# Import useful modules
import time
from typing import List, Tuple

import matplotlib.pyplot as plt  # graphing

# import numpy as np
import serial

import read_data
from read_data import Reading


def convert_reading_to_polar(reading: Reading) -> Tuple[List[float], List[int]]:
    """Convert a Reading object into a set of polar coordinates theta and r"""

    num_points = len(reading.points)
    start_angle = int(reading.start_angle)
    end_angle = int(reading.end_angle)
    step_size = int(((end_angle - start_angle) / num_points))
    # print(f"{start_angle=}, {end_angle=}, {step_size=}")
    angles = list(
        range(
            start_angle,
            end_angle,
            step_size,
        )
    )
    angles = angles[:-1]

    angles = [(each / 100) * 3.141529 / 180 for each in angles]  # convert to radians
    # The division by 100 because angle is given as, i.e., 32457 for 324.57 degrees

    distances = [each.distance for each in reading.points]

    return (angles, distances)


def main(ser: serial.Serial) -> None:

    # Initialize empty figure
    # fig: plt.Figure = plt.figure()
    # ax: plt.Axes = plt.axes(projection="3d")
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})

    # Initialize empty data lists
    angles: List[float] = []
    radii: List[int] = []

    while True:
        # print("Main loop")

        input: bytes = ser.read(1)  # read one byte
        # print(f"{input=}")
        if not input[0:1] == b"T":  # If that byte isn't a start character,
            continue  # repeat while loop, don't execute the code below

        s: bytes = ser.read(46)  # read the next 46 bytes

        # WARNING: I worry that in the time it takes to execute the character check
        # we might lose data, since the baud rate of the LD06 is so high.
        # That's why I tried the approach of grabbing a chunk of data and getting
        # as many complete packets out of it as I could.

        # print("Received the following data:")
        # print(s.hex())
        # print("Interpret data")
        # print(s)
        data: read_data.Reading = read_data.read_data(b"T" + s)

        # print(data)  # print to screen

        # ---------  DO YOUR DATA PROCESSING HERE --------------------

        # insert computations
        # print("Interpret")
        for each in data:
            new_angles, new_radii = convert_reading_to_polar(each)
            angles.extend(new_angles)
            radii.extend(new_radii)

        # ---------  DO YOUR GRAPHING AND GRAPH UPDATES HERE ---------
        # Display data
        print("Plot")
        print(f"{angles=}")
        print(f"{radii=}")
        ax.plot(angles, radii)
        ax.grid(True)
        fig.canvas.draw()
        fig.show()
        plt.pause(0.05)  # Note this 50 ms delay to prevent freezes
        time.sleep(1)


# Code that runs when file is directly executed, i.e.: `python serial_client.py`
if __name__ == "__main__":
    try:
        print("Starting")
        # Open serial port connection to LD06 LIDAR

        # with serial.serial_for_url("socket://DESKTOP-5PIT711:8000", timeout=1) as ser:
        with serial.Serial("COM4", 230400, timeout=1) as ser:
            print("Entered")
            # Run main data collection and processing loop
            main(ser)
            print("Exited")

    # Allow breaking the infinite loop
    except Exception as ex:
        print(ex)
    except KeyboardInterrupt as ex:
        print(ex)
