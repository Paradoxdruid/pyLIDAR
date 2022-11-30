"""pytest unit tests for read_data"""

import pytest

# Module to test
from pyLIDAR import read_data
from pyLIDAR.read_data import Point, Reading

# Constants
SAMPLE: bytes = bytes.fromhex(
    "54 2C 68 08 AB 7E E0 00 E4 DC 00 E2 D9 00 E5 D5 00 E3 D3 00 E4 D0 00 E9 CD 00"
    "E4 CA 00 E2 C7 00 E9 C5 00 E5 C2 00 E5 C0 00 E5 BE 82 3A 1A 50"
)

EXPECTED_READING: Reading = Reading(
    radar_speed=2152,
    start_angle=32427,
    end_angle=33470,
    timestamp=6714,
    points=[
        Point(distance=224, angle=32427.0, confidence=228),
        Point(distance=220, angle=32521.81818181818, confidence=226),
        Point(distance=217, angle=32616.636363636364, confidence=229),
        Point(distance=213, angle=32711.454545454544, confidence=227),
        Point(distance=211, angle=32806.27272727273, confidence=228),
        Point(distance=208, angle=32901.09090909091, confidence=233),
        Point(distance=205, angle=32995.90909090909, confidence=228),
        Point(distance=202, angle=33090.72727272727, confidence=226),
        Point(distance=199, angle=33185.545454545456, confidence=233),
        Point(distance=197, angle=33280.36363636364, confidence=229),
        Point(distance=194, angle=33375.181818181816, confidence=229),
        Point(distance=192, angle=33470.0, confidence=229),
    ],
)

EXPECTED_CHUNK: int = 84

# Tests


def test_read_data() -> None:

    actual: Reading = read_data.read_data(SAMPLE)
    assert actual == EXPECTED_READING


def test_read_data_failed_bytes() -> None:

    with pytest.raises(ValueError, match="Incomplete data packet."):
        _ = read_data.read_data(b"TT")


def test_read_data_failed_read() -> None:

    actual: Reading = read_data.read_data(SAMPLE[0:13] + b"TT" + SAMPLE[15:47])
    assert actual != EXPECTED_READING


def test_chunk() -> None:

    actual: int = read_data.chunk(SAMPLE[0:1])
    assert actual == EXPECTED_CHUNK
