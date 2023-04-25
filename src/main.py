import time
import logging


# File imports
import Connector
from websocket_client import WebSocketClient
from module.Camera import Camera




# Main program
def main():
    con = Connector.Connector()
    
    websocket_client = WebSocketClient()
    websocket_client.start()

    camera = Camera()
    
    if con.connected:
        try:
            while True:
                con.forward()
  
                data = con.read_data()

                if data == "CAPTURE":
                    print('Object detected! Capturing Image...')

                    camera.capture("test-image.jpg")

                # camera.start_preview()
                # camera.capture("test-image.jpg")
                # camera.start_preview()

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
