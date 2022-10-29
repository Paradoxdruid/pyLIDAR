# Use signal handling to break infinite loops
import signal
import sys
from types import FrameType
from typing import Optional

import serial

from pyLIDAR.pyLIDAR import main


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
