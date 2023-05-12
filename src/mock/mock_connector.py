class MockConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._configure_serial_connection()
        return cls._instance

    def _configure_serial_connection(self):
        self.connected = True

    def close(self):
        if self.connected:
            print("close")

    def __del__(self):
        self.close()

    def send_command(self, cmd):
        print(cmd)

    def forward(self):
        self.send_command("forward")

    def backward(self):
        self.send_command("backward")

    def left(self):
        self.send_command("left")

    def right(self):
        self.send_command("right")
    
    def start(self):
        self.send_command("start")

    def stop(self):
        self.send_command("stop")

    def drive_autonomously(self):
        self.send_command("auto")

    def drive_manually(self):
        self.send_command("manual")
