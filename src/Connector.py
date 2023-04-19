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

        # values = line.split(",")
        #
        # self.gyro["X"] = float(values[0][3:])
        # self.gyro["Y"] = float(values[1][3:])
        # self.gyro["Z"] = float(values[2][3:])

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
        self.send_command("t")
