from connections.base.base_connector import BaseConnector

class MockConnector(BaseConnector):
    def _configure_serial_connection(self):
        self.connected = True

    def close(self):
        if self.connected:
            print("Close Serial Connection")
            self.connected = False

    def __del__(self):
        self.close()
    
    def read_data(self):
        pass

    def write_data(self, data):
        pass

    def get_gyro_data(self):
        pass

    def send_command(self, cmd):
        print(cmd)

    def forward(self):
        self.send_command("Direction/Action: Forward")

    def backward(self):
        self.send_command("Direction/Action: Backward")

    def left(self):
        self.send_command("Direction/Action: Left")

    def right(self):
        self.send_command("Direction/Action: Right")
    
    def start(self):
        self.send_command("Action: Start")

    def stop(self):
        self.send_command("Action: Stop")

    def drive_autonomously(self):
        self.send_command("Driving Mode: Auto")

    def drive_manually(self):
        self.send_command("Driving Mode: Manual")
