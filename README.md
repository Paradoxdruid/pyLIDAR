# pyLIDAR

[![CodeFactor](https://www.codefactor.io/repository/github/paradoxdruid/pyLIDAR/badge)](https://www.codefactor.io/repository/github/paradoxdruid/pyLIDAR)  [![Codacy Badge](https://app.codacy.com/project/badge/Grade/c8c86fe25a644cb69b8b6e789ca1c18f)](https://www.codacy.com/gh/Paradoxdruid/pyLIDAR/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Paradoxdruid/pyLIDAR&amp;utm_campaign=Badge_Grade) ![CodeQL](https://github.com/Paradoxdruid/pyLIDAR/workflows/CodeQL/badge.svg) [![CI](https://github.com/Paradoxdruid/pyLIDAR/actions/workflows/CI.yml/badge.svg)](https://github.com/Paradoxdruid/pyLIDAR/actions/workflows/CI.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)  ![GitHub](https://img.shields.io/github/license/Paradoxdruid/pyLIDAR)

LDRobot makes a [LD06 LiDAR](https://www.ldrobot.com/product/en/98) sensor that has been widely adapted for applications such as Raspberry Pi.

This repository has some scripts to interact with the serial data from the LD06, making readings from the instrument available as well-structured dataclasses in Python, or automatically graphing input in real-time.

## Test pyLIDAR

In one shell, start the test server: `python pyLIDAR/example_server.py`

In another, start pyLIDAR, specifying the "test" port: `python pyLIDAR/pyLIDAR.py -p test --save --graph`

## Usage with LD06 LIDAR

In a shell, start pyLIDAR with appropriate port: `python pyLIDAR/pyLIDAR.py -p COM4 --save`

### Sample Output

![Sample Output](/assets/sample_output.png?raw=true "Sample Output")
