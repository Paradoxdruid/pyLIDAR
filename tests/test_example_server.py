"""pytest unit tests for example_server"""


# Module to test
from pyLIDAR import example_server
from pyLIDAR.read_data import Point, Reading

# Constants
SAMPLE: bytes = bytes.fromhex(
    (
        "54 2C 68 08 AB 7E E0 00 E4 DC 00 E2 D9 00 E5 D5 00 E3 D3 00 E4 D0 00 E9 CD 00"
        "E4 CA 00 E2 C7 00 E9 C5 00 E5 C2 00 E5 C0 00 E5 BE 82 3A 1A 50"
    )
)

EXPECTED_GENERATED_READING: Reading = Reading(
    radar_speed=100,
    start_angle=100,
    end_angle=5185,
    timestamp=100,
    points=[
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
        Point(distance=100, angle=200, confidence=100),
    ],
)

EXPECTED_CHUNK = "6808"

# Tests


def test_generate_reading(mocker) -> None:

    mocker.patch("pyLIDAR.example_server.randint", return_value=100)

    actual: Reading = example_server.generate_Reading()
    assert actual == EXPECTED_GENERATED_READING


def test_convert_chunk() -> None:
    actual: str = example_server.convert_chunk(2152)
    assert actual == EXPECTED_CHUNK
