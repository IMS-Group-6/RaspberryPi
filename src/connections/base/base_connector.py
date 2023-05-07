from abc import ABC, abstractmethod

class BaseConnector(ABC):
    _instance = None
    gyro = {
        "X": 0.0,
        "Y": 0.0,
        "Z": 0.0,
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._configure_serial_connection()
        return cls._instance

    @abstractmethod
    def _configure_serial_connection(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def write_data(self, data):
        pass
    
    @abstractmethod
    def get_gyro_data(self):
        pass

    @abstractmethod
    def send_command(self, cmd):
        pass

    @abstractmethod
    def forward(self):
        pass

    @abstractmethod
    def backward(self):
        pass

    @abstractmethod
    def left(self):
        pass

    @abstractmethod
    def right(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def drive_autonomously(self):
        pass

    @abstractmethod
    def drive_manually(self):
        pass
