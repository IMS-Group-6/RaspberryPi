import websocket
import json
import threading

SERVER_URL = "ws://localhost:8080"

'''''''''''
1. Initializes a WebSocketApp object with the specified server URL and sets up the event handlers for the WebSocket connection.
2. Starts the WebSocket connection in a separate thread to prevent blocking the main thread.
3. Sends initial data to the server when the connection is opened.
4. Receives and handles initial data from the server.
5. Handles errors and connection closure events.
'''''''''


class WebSocketClient:
    def __init__(self):
        self.ws = websocket.WebSocketApp(SERVER_URL,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close
                                         )
        self.ws.on_open = self.on_open

    def start(self):
        # Start the websocket connection in a separate thread
        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

    def on_open(self, *args):
        print("WebSocket connection opened")

        # Send initial data to the server
        initial_data = {"type": "initial_data", "data": "Hello, server!"}
        self.send(json.dumps(initial_data))

    def on_message(self, *args, **kwargs):
        message = args[1]
        print(f"Received message: {message}")

        # Handle received initial data from the server
        message_data = json.loads(message)
        if message_data.get("type") == "initial_data":
            print("Received initial data from the server")

    def on_error(self, *args):
        error = args[1]
        print(f"WebSocket error: {error}")

    def on_close(self, *args):
        print("WebSocket connection closed")

    def send(self, message):
        self.ws.send(message)


if __name__ == "__main__":
    client = WebSocketClient()
    client.start()
