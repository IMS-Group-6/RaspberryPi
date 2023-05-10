import logging
import asyncio
import threading

# File imports
from connections.mock.mock_connector import MockConnector
from connections.mock.mock_api_client import MockAPIClient
from connections.api_client import APIClient
from command_handler import CommandHandler

def main():
    global api_client, connector

    if connector.connected:
        print("Sending GET /ping")

        api_response = api_client.ping()
        if api_response.success:
            print("Successful...")
        else:
            print("Failed...")

if __name__ == "__main__":
    """
    This script sets up a mock connection to test the code without access to hardware. 

    Note that this test is still dependent on a backend connection, but it allows for testing the code in a 
    controlled environment without the need for actual hardware. It focuses on testing the socket.io commands.
    """
    logging.basicConfig(level=logging.ERROR)

    connector = MockConnector()
    api_client = MockAPIClient()
    # api_client = APIClient()
    command_handler = CommandHandler(api_client=api_client, connector=connector)

    t = threading.Thread(target=main, daemon=True)
    t.start()
    
    try:
        asyncio.run(command_handler.listen())
    except asyncio.exceptions.CancelledError:
        logging.info("Keyboard interrupt received, stopping...")
        if (connector.connected):

            # Stops an active session before program termination
            api_response = api_client.stop_mowing_session()

            if api_response.success:
                print(f"Stopped an active session before program termination, status code: {api_response.status_code}")
            elif not api_response.success and api_response.status_code == 400:
                print(f"No active session was found before program termination, status code: {api_response.status_code}")
            else:
                print(f"Failed to stop session, status code: {api_response.status_code}")
            
            connector.stop()
            connector.close()
