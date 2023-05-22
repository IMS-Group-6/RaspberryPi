import time
from picamera import PiCamera


class Camera:
    def __init__(self, resolution=(1024, 768)):
        """
        This function initializes a PiCamera object with a specified resolution.

        :param resolution: The resolution parameter is a tuple that specifies the width and height of the
        camera's image resolution. In this case, the default resolution is set to 1024 pixels wide and 768
        pixels high. This means that the camera will capture images with a resolution of 1024x768 pixels
        """
        self.camera = PiCamera()
        self.camera.resolution = resolution

    def start_preview(self):
        """
        This function starts the preview of the camera.
        """
        self.camera.start_preview()

    def stop_preview(self):
        """
        This function stops the camera preview.
        """
        self.camera.stop_preview()

    def capture(self, filename):
        """
        This function captures an image using a camera and saves it to a file with the given filename after
        a 2 second delay.

        :param filename: The filename parameter is a string that represents the name of the file where the
        captured image will be saved. It should include the file extension (e.g. ".jpg", ".png")
        """
        time.sleep(2)
        self.camera.capture(filename)
