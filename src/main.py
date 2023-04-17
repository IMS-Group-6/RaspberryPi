import time
import logging

# File imports
import Connector
from websocket_client import WebSocketClient


# Main program
def main():
    con = Connector.Connector()
    websocket_client = WebSocketClient()
    websocket_client.start()

    if con.connected:
        try:
            while True:
                # Here you can add your logic to decide which command to send
                # Example: forward for 2 seconds, then stop
                con.forward()
                time.sleep(1)
                con.backward()
                time.sleep(1)
                con.read_data()
                logging.debug(f"Gyro: {con.get_gyro_data()}")

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
