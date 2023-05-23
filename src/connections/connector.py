import serial
import time
import logging
from .base.base_connector import BaseConnector


class Connector(BaseConnector):
    def _configure_serial_connection(self):
        """
        This function configures a serial connection to a device and logs whether the connection was
        successful or not.
        """
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
        """
        This function closes a serial connection if it is currently open.
        """
        if self.connected:
            self.serialConnection.close()

    def __del__(self):
        """
        This is a destructor method in Python that calls the close() method to release resources when an
        object is destroyed.
        """
        self.close()

    def read_data(self):
        """
        This function reads data from a serial connection and parses it based on the first value in the
        comma-separated line.
        :return: different values depending on the content of the input line. If the line starts with
        "CAPTURE", it returns the line. If it starts with "ENCODER", it calls the parse_encoder method and
        returns "ENCODER". If it starts with "GYRO", it calls the parse_gyro method and returns "GYRO". If
        it doesn't match any of these cases it returns line.
        """
        try:
            line = self.serialConnection.readline().decode("utf-8").strip()
        except:
            return None

        # if line:
        #     logging.debug(line)

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
        """
        The function parses encoder data and updates the position of the left and right motors.

        :param line: The input string that contains encoder data
        """
        if line != ['']:
            data = list(map(int, line.split(",")[1:]))
            self.l = data[0] - self.lastPosL
            self.r = data[1] - self.lastPosR
            self.lastPosL = data[0]
            self.lastPosR = data[1]

    def parse_gyro(self, line):
        pass

    def get_gyro_data(self):
        """
        This function returns the gyro data.
        :return: The function `get_gyro_data` is returning the value of the `gyro` attribute of the object.
        """
        return self.gyro

    def write_data(self, data):
        """
        This function writes encoded data to a serial connection.

        :param data: The `data` parameter is a string that needs to be encoded in UTF-8 format before being
        written to a serial connection. The `write_data` method takes this encoded data and writes it to
        the serial connection
        """
        self.serialConnection.write(data.encode('utf-8'))

    def send_command(self, cmd):
        """
        This function sends a command and waits for 0.2 seconds before returning.

        :param cmd: The parameter "cmd" is a string that represents the command to be sent. This method
        "send_command" writes the command to a device and then waits for 0.2 seconds before returning
        """
        self.write_data(cmd)
        time.sleep(0.2)

    def forward(self):
        """
        This function writes the character "w" to a data stream.
        """
        self.write_data("w")

    def backward(self):
        """
        This function writes the character "s" to a data stream.
        """
        self.write_data("s")

    def left(self):
        """
        This function writes the character "a" to a data source.
        """
        self.write_data("a")

    def right(self):
        """
        This function writes the character "d" to a data source.
        """
        self.write_data("d")

    def start(self):
        """
        The "start" function writes the character "z" to some data.
        """
        self.write_data("z")

    def stop(self):
        """
        This function writes the character "x" to a data source.
        """
        self.write_data("x")

    def drive_autonomously(self):
        """
        The function "drive_autonomously" sends the command "t" to control the mower to drive
        autonomously.
        """
        self.write_data("t")

    def drive_manually(self):
        """
        This function writes the character "m" to indicate manual driving mode.
        """
        self.write_data("m")
