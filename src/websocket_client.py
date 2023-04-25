import websocket
from threading import Thread

class WebSocketClient:
    def __init__(self, connector):
        self.connector = connector
        self.ws_url = "ws://localhost:8080" # Replace with your WebSocket server URL
        self.ws = None

    def on_message(self, message):
        print(f"Received message: {message}")

        if message == "w":
            self.connector.forward()
        elif message == "s":
            self.connector.backward()
        elif message == "a":
            self.connector.left()
        elif message == "d":
            self.connector.right()
        elif message == "x":
            self.connector.stop()
        elif message == "q":
            self.connector.drive_autonomously()

    def on_error(self, error):
        print(f"WebSocket error: {error}")

    def on_close(self):
        print("WebSocket closed")

    def on_open(self):
        print("WebSocket opened")

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=lambda ws, msg: self.on_message(msg),
            on_error=lambda ws, err: self.on_error(err),
            on_close=lambda ws: self.on_close(),
        )

        self.ws.on_open = self.on_open
        thread = Thread(target=self.ws.run_forever)
        thread.start()