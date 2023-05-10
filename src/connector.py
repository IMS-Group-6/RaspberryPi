import serial
import time
import logging


class Connector:
    # Set up the serial port during Construction
    def __init__(self):
        self.gyro = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0,
        }
        self.lastPosL = 0
        self.lastPosR = 0
        self.l = 0
        self.r = 0

        # Configure the serial port
        logging.info("Connecting to device")
        try:
            self.serialConnection = serial.Serial(
                port='/dev/ttyUSB0',  # Replace with your serial port
                baudrate=115200,
                timeout=1
            )
            self.connected = True
            logging.info("Connection successful")

        except serial.SerialException:
            self.connected = False
            logging.error("Connection unsuccessful")

    def close(self):
        if self.connected:
            self.serialConnection.close()

    # Deconstruct
    def __del__(self):
        self.close()

    def read_data(self):
        line = self.serialConnection.readline().decode("utf-8").strip()
        if line:
            logging.debug(line)

        match line.split(',')[0].strip():
            case "CAPTURE":
                return line
            case "ENCODER":
                self.parse_encoder(line)
                return "ENCODER"
            case "GYRO":
                self.parse_gyro(line)
                return "GYRO"
            case _:
                return line

    def parse_encoder(self, line):
        if line != ['']:
            data = list(map(int, line))
            self.l = data[1] - self.lastPosL
            self.r = data[2] - self.lastPosR
            self.lastPosL = data[1]
            self.lastPosR = data[2]

    def parse_gyro(self, line):
        pass
    
    def write_data(self, data):
        self.serialConnection.write(data.encode('utf-8'))

    def get_gyro_data(self):
        return self.gyro

    def send_command(self, cmd):
        self.serialConnection.write(cmd.encode('utf-8'))
        time.sleep(0.2)

    def forward(self):
        self.send_command("w")

    def backward(self):
        self.send_command("s")

    def left(self):
        self.send_command("a")

    def right(self):
        self.send_command("d")

    def stop(self):
        self.send_command("x")

    def drive_autonomously(self):
        self.send_command("m")
