import requests
import logging
import config

class APIClient:
    server_url = config.SERVER_URL
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def ping(self):
        """
        Sends a GET request to the "/ping" endpoint to check if the API is up and running.

        Args:
        - None

        Returns:
        - True if the response status code is 200, indicating a successful request.
        - False if the response status code is not 200, indicating a failed request.
        """
        try:
            url = f"{self.server_url}/ping"
            response = requests.get(url)

            return response.status_code == 200
        except Exception as e:
            logging.error(e)
            return False
    
    def start_mowing_session(self):
        """
        Sends a POST request to the "/sessions/start" endpoint to start a mowing session.

        Args:
        - None

        Returns:
        - True if the response status code is 201, indicating a successful request.
        - False if the response status code is not 201, indicating a failed request.
        """
        try:
            url = f"{self.server_url}/sessions/start"
            response = requests.post(url)

            return response.status_code == 201
        except Exception as e:
            logging.error(e)
            return False     
    
    def stop_mowing_session(self):
        """
        Sends a POST request to the "/sessions/stop" endpoint to stop a mowing session.

        Args:
        - None

        Returns:
        - True if the response status code is 200, indicating a successful request.
        - False if the response status code is not 200, indicating a failed request.
        """
        try:
            url = f"{self.server_url}/sessions/stop"
            response = requests.post(url)

            return response.status_code == 200
        except Exception as e:
            logging.error(e)
            return False     
    
    def post_position(self, x, y):
        """
        Sends a POST request to the "/coordinates/positions" endpoint to post the current position of the mower.

        Args:
        - x: An int representing the x-coordinate of the mower's position.
        - y: An int representing the y-coordinate of the mower's position.

        Returns:
        - True if the response status code is 201, indicating a successful request.
        - False if the response status code is not 201, indicating a failed request.
        """
        try:
            url = f"{self.server_url}/coordinates/positions"

            coordinates = { "x": x, "y": y }
            response = requests.post(url, data=coordinates)

            return response.status_code == 201
        except Exception as e:
            logging.error(e)
            return False
    
    def post_boundary(self, x, y):
        """
        Sends a POST request to the "/coordinates/boundaries" endpoint to post the coordinates of a boundary.

        Args:
        - x: An int representing the x-coordinate of the boundary.
        - y: An int representing the y-coordinate of the boundary.

        Returns:
        - True if the response status code is 201, indicating a successful request.
        - False if the response status code is not 201, indicating a failed request.
        """
        try:
            url = f"{self.server_url}/coordinates/boundaries"

            coordinates = { "x": x, "y": y }
            response = requests.post(url, data=coordinates)

            return response.status_code == 201
        except Exception as e:
            logging.error(e)
            return False

    def post_obstacle(self, x, y, image):
        """
        Sends a POST request to the "/coordinates/obstacles" endpoint to post the coordinates and image of an obstacle.

        Args:
        - x: An int representing the x-coordinate of the obstacle.
        - y: An int representing the y-coordinate of the obstacle.
        - image: A string representing the filename (including path) of the obstacle image.

        Returns:
        - True if the response status code is 201, indicating a successful request.
        - False if the response status code is not 201, indicating a failed request.
        """
        try:
            url = f"{self.server_url}/coordinates/obstacles"

            with open(image, 'rb') as image_file:
                image_content = image_file.read()

            coordinates = { "x": x, "y": y }
            captured_image = { "image": ('obstacle.jpg', image_content) } 
            response = requests.post(url, data=coordinates, files=captured_image)

            return response.status_code == 201
        except Exception as e:
            logging.error(e)
            return False
