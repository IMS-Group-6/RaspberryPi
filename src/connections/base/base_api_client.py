from abc import ABC, abstractmethod
import config

class ApiResponse:
    def __init__(self, success, status_code):
        self.success: bool = success
        self.status_code: int = status_code

class BaseAPIClient(ABC):
    _instance = None
    server_url = config.SERVER_URL

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def ping(self) -> ApiResponse:
        """
        Sends a GET request to the "/ping" endpoint to check if the API is up and running.

        Args:
        - None

        Returns:
        - ApiResponse object with success=True if the response status code is 200, indicating a successful request.
        - ApiResponse object with success=False if the response status code is not 200, indicating a failed request.
        """
        pass

    @abstractmethod
    def start_mowing_session(self) -> ApiResponse:
        """
        Sends a POST request to the "/sessions/start" endpoint to start a mowing session.

        Args:
        - None

        Returns:
        - ApiResponse object with success=True if the response status code is 201, indicating a successful request.
        - ApiResponse object with success=False if the response status code is not 201, indicating a failed request.
        """
        pass

    @abstractmethod
    def stop_mowing_session(self) -> ApiResponse:
        """
        Sends a POST request to the "/sessions/stop" endpoint to stop a mowing session.

        Args:
        - None

        Returns:
        - ApiResponse object with success=True if the response status code is 200, indicating a successful request.
        - ApiResponse object with success=False if the response status code is not 200, indicating a failed request.
        """
        pass

    @abstractmethod
    def post_position(self, x, y) -> ApiResponse:
        """
        Sends a POST request to the "/coordinates/positions" endpoint to post the current position of the mower.

        Args:
        - x: An int representing the x-coordinate of the mower's position.
        - y: An int representing the y-coordinate of the mower's position.

        Returns:
        - ApiResponse object with success=True if the response status code is 201, indicating a successful request.
        - ApiResponse object with success=False if the response status code is not 201, indicating a failed request.
        """
        pass

    @abstractmethod
    def post_boundary(self, x, y) -> ApiResponse:
        """
        Sends a POST request to the "/coordinates/boundaries" endpoint to post the coordinates of a boundary.

        Args:
        - x: An int representing the x-coordinate of the boundary.
        - y: An int representing the y-coordinate of the boundary.

        Returns:
        - ApiResponse object with success=True if the response status code is 201, indicating a successful request.
        - ApiResponse object with success=False if the response status code is not 201, indicating a failed request.
        """
        pass

    @abstractmethod
    def post_obstacle(self, x, y, image) -> ApiResponse:
        """
        Sends a POST request to the "/coordinates/obstacles" endpoint to post the coordinates and image of an obstacle.

        Args:
        - x: An int representing the x-coordinate of the obstacle.
        - y: An int representing the y-coordinate of the obstacle.
        - image: A string representing the filename (including path) of the obstacle image.

        Returns:
        - ApiResponse object with success=True if the response status code is 201, indicating a successful request.
        - ApiResponse object with success=False if the response status code is not 201, indicating a failed request.
        """
        pass
