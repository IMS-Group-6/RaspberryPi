import requests
import logging
# from src.connections.base.base_api_client import ApiResponse, BaseAPIClient
from .base.base_api_client import ApiResponse, BaseAPIClient


class APIClient(BaseAPIClient):
    def ping(self):
        """
        This function sends a ping request to a server and returns an ApiResponse object indicating whether
        the request was successful or not.
        :return: The `ping` method returns an `ApiResponse` object. The `ApiResponse` object contains a
        boolean value indicating whether the status code returned from the server is 200 (True if it is,
        False otherwise), and the status code itself. If an exception occurs during the request, the method
        returns an `ApiResponse` object with a False boolean value and a None status code.
        """
        try:
            url = f"{self.server_url}/ping"
            status_code = requests.get(url).status_code

            return ApiResponse(status_code == 200, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)

    def start_mowing_session(self):
        """
        This function starts a mowing session by sending a POST request to a server URL and returns an
        ApiResponse object indicating the success or failure of the request.
        :return: The `start_mowing_session` method returns an `ApiResponse` object. The `ApiResponse` object
        contains a boolean value indicating whether the request was successful or not, and a status code. If
        the request was successful, the boolean value will be `True` and the status code will be `201`. If
        the request was not successful, the boolean value will be `False` and the status code
        """
        try:
            url = f"{self.server_url}/sessions/start"
            status_code = requests.post(url).status_code

            return ApiResponse(status_code == 201, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)

    def stop_mowing_session(self):
        """
        This function sends a POST request to stop a mowing session and returns an ApiResponse object
        indicating success or failure.
        :return: an instance of the `ApiResponse` class. The `ApiResponse` object contains a boolean value
        indicating whether the request was successful or not, and a status code indicating the HTTP status
        code of the response. If an exception occurs during the request, the function returns an
        `ApiResponse` object with a `False` boolean value and `None` status code.
        """
        try:
            url = f"{self.server_url}/sessions/stop"
            status_code = requests.post(url).status_code

            return ApiResponse(status_code == 200, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)

    def post_position(self, x, y):
        """
        This function sends a POST request to a server with x and y coordinates and returns an ApiResponse
        object indicating the success or failure of the request.
        """
        try:
            url = f"{self.server_url}/coordinates/positions"

            coordinates = {"x": x, "y": y}
            status_code = requests.post(url, data=coordinates).status_code

            return ApiResponse(status_code == 201, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)

    def post_boundary(self, x, y):
        """
        This function sends a POST request to a server with x and y coordinates to update the boundaries.
        """
        try:
            url = f"{self.server_url}/coordinates/boundaries"

            coordinates = {"x": x, "y": y}
            status_code = requests.post(url, data=coordinates).status_code

            return ApiResponse(status_code == 201, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)

    def post_obstacle(self, x, y, image):
        """
        The function posts an obstacle's coordinates and image to a server URL.
        """
        try:
            url = f"{self.server_url}/coordinates/obstacles"

            with open(image, 'rb') as image_file:
                image_content = image_file.read()

            coordinates = {"x": x, "y": y}
            captured_image = {"image": ('obstacle.jpg', image_content)}
            status_code = requests.post(
                url, data=coordinates, files=captured_image).status_code

            return ApiResponse(status_code == 201, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)
