import asyncio
import websockets

async def handle_client(websocket, path):
    print("Client connected")
    
    try:
        while True:
            command = input("Enter a command: ")
            await websocket.send(command)
    except websocket.exceptions.ConnectionClosedError:
        print("Client disconnected")

start_server = websockets.serve(handle_client, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
