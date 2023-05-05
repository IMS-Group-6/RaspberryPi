import logging
import asyncio
import threading

# File imports
from connections.api_client import APIClient
from command_handler import CommandHandler
from mock.mock_connector import MockConnector
import config

def main():
    api_client = APIClient()
    con = MockConnector()

    if con.connected:
        print(f"Sending GET /ping to {config.SERVER_URL}")

        if api_client.ping():
            print("Successful...")
        else:
            print("Failed...")


if __name__ == "__main__":
    """
    This script sets up a mock connection to test the code without access to hardware. 

    Note that this test is still dependent on a backend connection, but it allows for testing the code in a 
    controlled environment without the need for actual hardware. It focuses on testing the socket.io commands.
    """
    t = threading.Thread(target=main, daemon=True)
    t.start()
    
    con = MockConnector()
    api_client = APIClient()
    command_handler = CommandHandler(connector=con)

    try:
        asyncio.run(command_handler.listen())
    except asyncio.exceptions.CancelledError:
        logging.info("Keyboard interrupt received, stopping...")
        if (con.connected):
            print("\n----")
            
            # Stops an active session before program termination
            if api_client.stop_mowing_session():
                print("Stopped an active session before program termination")
            else:
                print("No active session was found before program termination")
            
            con.stop()
            con.close()
