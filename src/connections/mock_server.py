import asyncio
import socketio
'''''''''
1. connect: When a client connects to the server, this handler is triggered, and the server prints the client's session ID.
2. disconnect: When a client disconnects from the server, this handler is triggered, and the server prints the client's session ID.
3. message: When a message is received from a client, this handler is triggered. The server prints the received message and sends a hardcoded command back to the client using the sio.emit() function.
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
    await sio.emit('message', '{"type": "MOWER_COMMAND", "data": {"direction": "forward"}}', to=sid)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=3000)
