import asyncio
import json
import websockets

pc_clients = set()
flutter_clients = set()

async def handle_pc(websocket):
    print("[INFO] PC connected")
    pc_clients.add(websocket)
    try:
        async for message in websocket:
            # إعادة البث لجميع عملاء Flutter
            for client in flutter_clients:
                await client.send(message)
    finally:
        pc_clients.remove(websocket)
        print("[INFO] PC disconnected")

async def handle_flutter(websocket):
    print("[INFO] Flutter connected")
    flutter_clients.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        flutter_clients.remove(websocket)
        print("[INFO] Flutter disconnected")

async def main(websocket, path):
    if path == "/pc":
        await handle_pc(websocket)
    elif path == "/flutter":
        await handle_flutter(websocket)
    else:
        await websocket.close()

start_server = websockets.serve(main, "0.0.0.0", 10000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
