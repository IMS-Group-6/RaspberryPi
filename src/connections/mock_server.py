import asyncio
import socketio
'''''''''
This test server listens for incoming connections, and when a client connects, it stores its SID(session ID). 
You can send hard-coded commands to the connected client by typing them in the terminal(e.g., forward, backward, left, right). 
The server will send the command as a MOWER_COMMAND event to the connected client.
'''''''''
sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)


@sio.event
async def disconnect(sid):
    print('Client disconnected:', sid)


@sio.event
async def message(sid, data):
    print(f"Received message from {sid}: {data}")

    # Example of sending a hardcoded command to the client
    await sio.emit('message', '{"type": "MOWER_COMMAND", "data": {"direction": "left"}}', to=sid)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=3000)
