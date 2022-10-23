"""Interpret LD06 LIDAR data packets"""

from dataclasses import dataclass
from typing import List

SAMPLE = bytes.fromhex(
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
    points: List[Point]


def chunk(byte_input: bytes) -> int:
    """Convert given byte(s) to int representation"""
    return int.from_bytes(byte_input, "big")


def read_data(raw_bytes: bytes) -> List[Reading]:
    """Convert data packet into a list of Readings"""

    bytes_split = raw_bytes.split(b"T")

    readings_list: List[Reading] = []
    for each_bytes in bytes_split:
        # print(each.hex())
        if len(each_bytes) != 46:  # Ignore incomplete reads
            continue

        # Analyze each complete reading
        each_bytes = b"T" + each_bytes  # Put back the start character that was stripped

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

        readings_list.append(
            Reading(
                radar_speed=radar_speed,
                start_angle=start_angle,
                end_angle=end_angle,
                timestamp=timestamp,
                points=out_data,
            )
        )

    return readings_list


if __name__ == "__main__":
    print(read_data(SAMPLE)[0])

    assert str(read_data(SAMPLE)[0]) == (
        "Reading(radar_speed=2152, start_angle=32427, end_angle=33470, "
        "timestamp=6714, points=[Point(distance=224, angle=32427.0, confidence=228), "
        "Point(distance=220, angle=32521.81818181818, confidence=226), "
        "Point(distance=217, angle=32616.636363636364, confidence=229), "
        "Point(distance=213, angle=32711.454545454544, confidence=227), "
        "Point(distance=211, angle=32806.27272727273, confidence=228), "
        "Point(distance=208, angle=32901.09090909091, confidence=233), "
        "Point(distance=205, angle=32995.90909090909, confidence=228), "
        "Point(distance=202, angle=33090.72727272727, confidence=226), "
        "Point(distance=199, angle=33185.545454545456, confidence=233), "
        "Point(distance=197, angle=33280.36363636364, confidence=229), "
        "Point(distance=194, angle=33375.181818181816, confidence=229), "
        "Point(distance=192, angle=33470.0, confidence=229)])"
    ), "Reading is not identical"
