import serial
import time
import logging
from .base.base_connector import BaseConnector

class Connector(BaseConnector):
    def _configure_serial_connection(self):
        logging.info(f"{self.__class__.__name__}: Connecting to device")
        try:
            self.serialConnection = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=115200,
                timeout=1
            )
            self.connected = True
            logging.info(f"{self.__class__.__name__}: Connection successful")

        except serial.SerialException:
            self.connected = False
            logging.info(f"{self.__class__.__name__}: Connection unsuccessful")

    def close(self):
        if self.connected:
            self.serialConnection.close()

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

    def get_gyro_data(self):
        return self.gyro

    def write_data(self, data):
        self.serialConnection.write(data.encode('utf-8'))

    def send_command(self, cmd):
        self.write_data(cmd)
        time.sleep(0.2)

    def forward(self):
        self.write_data("w")

    def backward(self):
        self.write_data("s")

    def left(self):
        self.write_data("a")

    def right(self):
        self.write_data("d")
    
    def start(self):
        self.write_data("z")

    def stop(self):
        self.write_data("x")

    def drive_autonomously(self):
        self.write_data("t")

    def drive_manually(self):
        self.write_data("m")
