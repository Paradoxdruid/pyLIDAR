# Attempt at implementing polar coordinates

from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from read_data import Point, Reading

SAMPLE: List[Reading] = [
    Reading(
        radar_speed=2152,
        start_angle=32427,
        end_angle=33470,
        timestamp=6714,
        points=[
            Point(distance=224, confidence=228),
            Point(distance=220, confidence=226),
            Point(distance=217, confidence=229),
            Point(distance=213, confidence=227),
            Point(distance=211, confidence=228),
            Point(distance=208, confidence=233),
            Point(distance=205, confidence=228),
            Point(distance=202, confidence=226),
            Point(distance=199, confidence=233),
            Point(distance=197, confidence=229),
            Point(distance=194, confidence=229),
            Point(distance=192, confidence=229),
        ],
    )
]


def convert_reading_to_polar(reading: Reading) -> Tuple[List[float], List[int]]:
    """Convert a Reading object into a set of polar coordinates theta and r"""

    num_points = len(reading.points)
    start_angle = int(reading.start_angle)
    end_angle = int(reading.end_angle)
    step_size = int(((end_angle - start_angle) / num_points))
    print(f"{start_angle=}, {end_angle=}, {step_size=}")
    angles = list(
        range(
            start_angle,
            end_angle,
            step_size,
        )
    )
    angles = angles[:-1]

    angles = [(each / 100) * np.pi / 180 for each in angles]  # convert to radians
    # The division by 100 because angle is given as, i.e., 32457 for 324.57 degrees

    distances = [each.distance for each in reading.points]

    return (angles, distances)


def plot_polar_coords(angles: List[float], distances: List[int]) -> None:
    """Plot a set of theta and r polar coordinates and save as an image"""

    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    ax.plot(angles, distances)
    # ax.set_rmax(2)
    # ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)

    ax.set_title("A polar plot of sample reading data", va="bottom")
    plt.savefig("example_polar.png")


if __name__ == "__main__":
    angles, distances = convert_reading_to_polar(SAMPLE[0])
    plot_polar_coords(angles, distances)
