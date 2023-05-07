import serial
import time
import logging
from connections.base.base_connector import BaseConnector

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
        return line

    def write_data(self, data):
        self.serialConnection.write(data.encode('utf-8'))

    def get_gyro_data(self):
        return self.gyro

    def send_command(self, cmd):
        self.write_data(cmd)
        time.sleep(0.2)

    def forward(self):
        self.send_command("w")

    def backward(self):
        self.send_command("s")

    def left(self):
        self.send_command("a")

    def right(self):
        self.send_command("d")
    
    def start(self):
        self.send_command("z")

    def stop(self):
        self.send_command("x")

    def drive_autonomously(self):
        self.send_command("t")

    def drive_manually(self):
        self.send_command("m")
