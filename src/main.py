import logging
import asyncio

# File imports
from module.Camera import Camera
from connections.api_client import APIClient
from connections.connector import Connector
from command_handler import CommandHandler


async def main():
    con = Connector()
    camera = Camera()
    
    api_client = APIClient()
    command_handler = CommandHandler()
    await command_handler.listen()

    if con.connected:
        try:
            while True:
                # Should boundary and obstacle events be sent from here?
                data = con.read_data()

                if data == "CAPTURE":
                    print('Object detected! Capturing Image...')
                    # This is the function which will capture an image and store it to the local folder if nothing else is entered
                    camera.capture("test-image.jpg")

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
