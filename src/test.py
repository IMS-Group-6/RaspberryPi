import logging
import asyncio
import threading
from time import sleep

# File imports
from connections.api_client import APIClient
from command_handler import CommandHandler
import config

def main():
    api_client = APIClient()

    if True:
        while True:
            print(f"Sending GET /ping to {config.SERVER_URL}")
            api_client.ping()
            sleep(10)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    t = threading.Thread(target=main, daemon=True)
    t.start()
    
    con = "test"
    command_handler = CommandHandler(connector=con)
    try:
        asyncio.run(command_handler.listen())
    except asyncio.exceptions.CancelledError:
        logging.info("Keyboard interrupt received, stopping...")
