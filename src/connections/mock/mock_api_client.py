from connections.api_client import ApiResponse
from connections.base.base_api_client import BaseAPIClient

class MockAPIClient(BaseAPIClient):
    is_session_active = False

    def ping(self):
        return ApiResponse(True, 200)

    def start_mowing_session(self):
        if self.is_session_active:
            return ApiResponse(False, 400)
        
        self.is_session_active = True
        return ApiResponse(True, 201)

    def stop_mowing_session(self):
        if self.is_session_active:
            self.is_session_active = False
            return ApiResponse(True, 200)
        
        return ApiResponse(True, 404)

    def post_position(self, x, y):
        return ApiResponse(True, 201)

    def post_boundary(self, x, y):
        return ApiResponse(True, 201)

    def post_obstacle(self, x, y, image):
        return ApiResponse(True, 201)
