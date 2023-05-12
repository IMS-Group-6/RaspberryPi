import requests
import logging
from connections.base.base_api_client import ApiResponse, BaseAPIClient

class APIClient(BaseAPIClient):
    def ping(self):
        try:
            url = f"{self.server_url}/ping"
            status_code = requests.get(url).status_code
            
            return ApiResponse(status_code == 200, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)
    
    def start_mowing_session(self):
        try:
            url = f"{self.server_url}/sessions/start"
            status_code = requests.post(url).status_code

            return ApiResponse(status_code == 201, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)   
    
    def stop_mowing_session(self):
        try:
            url = f"{self.server_url}/sessions/stop"
            status_code = requests.post(url).status_code

            return ApiResponse(status_code == 200, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)
    
    def post_position(self, x, y):
        try:
            url = f"{self.server_url}/coordinates/positions"

            coordinates = { "x": x, "y": y }
            status_code = requests.post(url, data=coordinates).status_code

            return ApiResponse(status_code == 201, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)
    
    def post_boundary(self, x, y):
        try:
            url = f"{self.server_url}/coordinates/boundaries"

            coordinates = { "x": x, "y": y }
            status_code = requests.post(url, data=coordinates).status_code

            return ApiResponse(status_code == 201, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)

    def post_obstacle(self, x, y, image):
        try:
            url = f"{self.server_url}/coordinates/obstacles"

            with open(image, 'rb') as image_file:
                image_content = image_file.read()

            coordinates = { "x": x, "y": y }
            captured_image = { "image": ('obstacle.jpg', image_content) } 
            status_code = requests.post(url, data=coordinates, files=captured_image).status_code

            return ApiResponse(status_code == 201, status_code)
        except Exception as e:
            logging.error(e)
            return ApiResponse(False, None)
