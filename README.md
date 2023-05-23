# Autonomous Lawn Mower

This project controls an autonomous lawn mower via a Raspberry Pi. The mower can be operated in two modes - automatic and manual. It communicates with a server to send its coordinates and captured images of obstacles. The mower can be controlled remotely through commands sent from the mobile application through the server.

## Installation Requirements

**Hardware**:

- Raspberry Pi
- mbot ranger (configured to work with Raspberry Pi)
- PiCamera

**Software**:

- `Python 3.9+, aiohttp, socketio, requests, picamera, and pyserial Python libraries.`

## Setup and Installation

- Clone this repository to your Raspberry Pi.
- Install the necessary Python libraries using pip:

```
pip install -r requirements.txt
```

- Configure your Raspberry Pi to connect with your lawn mower.
- Update config.py with your server URL.

## Project Structure

The main components of this project are:

- **command_handler.py**: Listens for commands from the API and executes them using the Connector class.
- **api_client.py**: Handles communication with the API.
- **connector.py**: Manages the serial connection with the Arduino and sends/receives data.
- **map.py**: Manages a set of 2D points, performs geometric calculations, and transmits the points to the backend.
- **odometry.py**: Uses encoder data to calculate the position of the robot.
- **Camera.py**: Captures images using the robot's camera.
- **mock_connector.py and mock_api_client.py**: Mock classes for testing the system without a physical robot or an API.

## Usage

To run the main program, execute the main.py script. This will start listening for commands from the API and handling them accordingly.

```
python3 main.py
```

If you want to run the system with mock components for testing, you can run the test.py script.

```
python3 test.py
```

The lawn mower will now connect to your server and can be controlled via the server.

The mower understands the following commands:

- **forward**: Move forward
- **backward**: Move backward
- **left**: Turn left
- **right**: Turn right
- **start**: Start mowing
- **stop**: Stop mowing

The mower can operate in two modes - **auto** and **manual**. In **auto** mode, the mower operates autonomously, making its own decisions based on the input from its sensors. In **manual** mode, the mower needs to be controlled via commands from the server.

## API Endpoints

This project communicates with the server via the following endpoints:

- **GET /ping**: Check if the server is online.
- **POST /sessions/start**: Start a new mowing session.
- **POST /sessions/stop**: Stop the current mowing session.
- **POST /coordinates/positions**: Post the current position of the mower.
- **POST /coordinates/boundaries**: Post the boundary coordinates.
- **POST /coordinates/obstacles**: Post coordinates of obstacles and their images.
