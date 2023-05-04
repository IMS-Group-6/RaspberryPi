import logging
import asyncio
import threading
from time import sleep

# File imports
from connections.api_client import APIClient
from command_handler import CommandHandler
from mock.mock_connector import MockConnector
import config

def main():
    api_client = APIClient()
    con = MockConnector()

    if con.connected:
        while True:
            print(f"Sending GET /ping to {config.SERVER_URL}")

            if api_client.ping():
                print("Successful...")
            else:
                print("Failed...")
            
            sleep(30)

if __name__ == "__main__":
    """
    This script sets up a mock connection to test the code without access to hardware. 

    Note that this test is still dependent on a backend connection, but it allows for testing the code in a 
    controlled environment without the need for actual hardware. It focuses on testing the socket.io commands.
    """
    t = threading.Thread(target=main, daemon=True)
    t.start()
    
    con = MockConnector()
    command_handler = CommandHandler(connector=con)
    try:
        asyncio.run(command_handler.listen())
    except asyncio.exceptions.CancelledError:
        logging.info("Keyboard interrupt received, stopping...")
        if (con.connected):
            print("\n----")
            con.stop()
            con.close()
