import requests

class APIClient:
    def __init__(self, url):
        self.url = url
    
    def ping(self):
        """
        Sends a ping request.
        """
        try:
            url = f"{self.url}/ping"

            response = requests.get(url)
            print(response.text)

        except Exception as e:
            print('Error: ', e)
    
    def send_obstacle(self, session_id, x, y, image):
        """
        Sends a collision avoidance event.
        """
        try:
            url = f"{self.url}/coordinates/obstacles"

            # Example
            with open(image, 'rb') as image_file:
                image_content = image_file.read()

            coordinates = { "sessionId": session_id, "x": x, "y": y}
            captured_image = { "image": ('image.jpg', image_content) } 
            response = requests.post(url, data=coordinates, files=captured_image)

            print(response.status_code)
            print(response.text)

        except Exception as e:
            print('Error: ', e)



client = APIClient("http://localhost:8080")
client.ping()
# client.send_obstacle('clgfom3az0002rqah3kt4kbxi',1, 2, 'cat.jpeg')
