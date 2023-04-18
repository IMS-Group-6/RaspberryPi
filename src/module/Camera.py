import time
from picamera import PiCamera

class Camera:
    def __init__(self, resolution=(1024, 768)):
        self.camera = PiCamera()
        self.camera.resolution = resolution

    def start_preview(self):
        self.camera.start_preview()

    def stop_preview(self):
        self.camera.stop_preview()

    def capture(self, filename):
        time.sleep(2)
        self.camera.capture(filename)

