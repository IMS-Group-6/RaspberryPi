# Library imports
import logging
import asyncio
import threading
from datetime import datetime
import os

# File imports
from odometry import Odemetry
from module.Camera import Camera
from connections.api_client import APIClient
from connections.connector import Connector
from command_handler import CommandHandler


def main():
    global api_client, con, odom

    odom = Odemetry()

    camera = Camera()

    if con.connected:
        while True:
            # Should boundary and obstacle events be sent from here?
            data = con.read_data()

            match data:
                case "CAPTURE":
                    print("Collision... Capturing Image")
                    camera.capture("image.jpg")
                    api_client.post_obstacle(odom.x, odom.y, "image.jpg")
                    os.remove("image.jpg")
                case "ENCODER":
                    odom.solve(con.l, con.r)
                # case "BORDER":
                #    odom.border()
                #    point = odom.map.getNextPoint()
                #    api_client.post_boundary(point.x, point.y)
                case _:
                    pass


async def odometry_poster():
    while con.connected:
        api_client.post_position(odom.x, odom.y)
        await asyncio.sleep(1)


async def main_async():
    await asyncio.gather(
        command_handler.listen(),
        odometry_poster()
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    api_client = APIClient()
    con = Connector()
    command_handler = CommandHandler(api_client=api_client, connector=con)

    # Start the main() function in a separate thread
    t = threading.Thread(target=main, daemon=True)
    t.start()

    try:
        asyncio.run(main_async())
    except asyncio.exceptions.CancelledError:
        logging.info("Keyboard interrupt received, stopping...")
        if (con.connected):

            # Stops an active session before program termination
            api_response = api_client.stop_mowing_session()

            if api_response.success:
                print(f"Stopped an active session before program termination, status code: {api_response.status_code}")
            elif not api_response.success and api_response.status_code == 400:
                print(
                    f"No active session was found before program termination, status code: {api_response.status_code}")
            else:
                print(f"Failed to stop session, status code: {api_response.status_code}")

            con.stop()
            con.close()
