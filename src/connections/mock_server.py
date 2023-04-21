import asyncio
import socketio
import json

'''''''''
This test server listens for incoming connections, and when a client connects, it stores its SID(session ID). 
You can send hard-coded commands to the connected client by typing them in the terminal(e.g., forward, backward, left, right). 
The server will send the command as a MOWER_COMMAND event to the connected client.
'''''''''

# Setup Socket.IO server
sio = socketio.AsyncServer(async_mode='aiohttp')
app = socketio.AsyncApp(server=sio)

# Store the connected mower's SessionID
mower_sid = None

# Event handler for new connections


@sio.event
async def connect(sid, environ):
    global mower_sid
    print(f"Client connected: {sid}")
    mower_sid = sid

# Event handler for disconnections


@sio.event
async def disconnect(sid):
    global mower_sid
    print(f"Client disconnected: {sid}")
    if sid == mower_sid:
        mower_sid = None

# Event handler for incoming messages


@sio.on("message")
async def message(sid, data):
    print(f"Message from {sid}: {data}")


async def send_command(command):
    global mower_sid
    if mower_sid:
        data = {
            "type": "MOWER_COMMAND",
            "data": {
                "direction": command
            }
        }
        await sio.emit("message", json.dumps(data), to=mower_sid)
    else:
        print("Mower is not connected.")


async def main():
    # Start the server
    runner = socketio.AsyncRunner(app, host='localhost', port=8080)
    await runner.setup()
    await runner.server.start_runner()

    try:
        while True:
            command = input("Enter command (forward, backward, left, right): ")
            if command in ["forward", "backward", "left", "right"]:
                await send_command(command)
            else:
                print("Invalid command. Try again.")
    except KeyboardInterrupt:
        print("Shutting down server...")
        await runner.server.cleanup()

if __name__ == '__main__':
    asyncio.run(main())
