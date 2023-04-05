import serial
import time


class Connector:
    # Set up the serial port during Construction
    def __init__(self):
        # Configure the serial port
        try:
            self.serialConnection = serial.Serial(
                port='/dev/ttyACM0',  # Replace with your serial port
                baudrate=9600,
                timeout=1
            )
            self.connected = True

        except serial.SerialException:
            self.connected = False

    def close(self):
        if self.connected:
            self.serialConnection.close()

    # Deconstruct
    def __del__(self):
        self.close()

    def send_command(self, cmd):
        self.serialConnection.write(cmd.encode('utf-8'))
        time.sleep(0.2)

    def forward(self):
        self.send_command("w\n")

    def backward(self):
        self.send_command("s\n")

    def left(self):
        self.send_command("a\n")

    def right(self):
        self.send_command("d\n")

    def stop(self):
        self.send_command("stop\n")
