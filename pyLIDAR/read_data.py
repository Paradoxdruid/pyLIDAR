"""Interpret LD06 LIDAR data packets"""

from dataclasses import dataclass


@dataclass
class Point:
    """Individual data point"""

    distance: int
    angle: float
    confidence: int


@dataclass
class Reading:
    """Complete reading from a single data packet"""

    radar_speed: int
    start_angle: int
    end_angle: int
    timestamp: int
    points: list[Point]


def chunk(byte_input: bytes) -> int:
    """Convert given byte(s) to int representation"""
    return int.from_bytes(byte_input, "big")


def read_data(each_bytes: bytes) -> Reading:
    """Convert data packet into a Reading"""

    if len(each_bytes) != 47:  # raise on incomplete reads
        raise ValueError("Incomplete data packet.")

    # Analyze each complete reading
    radar_speed = chunk(each_bytes[3:4] + each_bytes[2:3])
    start_angle = chunk(each_bytes[5:6] + each_bytes[4:5])
    data = each_bytes[6:42]
    end_angle = chunk(each_bytes[43:44] + each_bytes[42:43])
    timestamp = chunk(each_bytes[45:46] + each_bytes[44:45])
    # crc_check = chunk(input[46:47])

    data_list = [data[i : i + 3] for i in range(0, len(data), 3)]

    if end_angle > start_angle:  # Calculate Angle Increment
        angle_inc = (end_angle - start_angle) / 11
    else:
        angle_inc = (end_angle + 36000 - start_angle) / 11

    angles = [start_angle + i * angle_inc for i in range(0, 12)]

    out_data = [
        Point(
            distance=chunk(each[1:2] + each[0:1]),
            angle=angle,
            confidence=chunk(each[2:3]),
        )
        for (each, angle) in zip(data_list, angles)
    ]

    return Reading(
        radar_speed=radar_speed,
        start_angle=start_angle,
        end_angle=end_angle,
        timestamp=timestamp,
        points=out_data,
    )
