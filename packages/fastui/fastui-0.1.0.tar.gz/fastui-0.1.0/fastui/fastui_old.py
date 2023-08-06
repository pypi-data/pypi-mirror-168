from fastapi import FastAPI, WebSocket, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

store = {
    "count": 0
}

async def message_handler(data, websocket):
    from pprint import pprint
    pprint(store)
    if data == 'i':
        store["count"] += 1
        await websocket.send_text(str(store["count"]))
        print("Count incremented")

    elif data == 'd':
        store["count"] -= 1
        await websocket.send_text(str(store["count"]))
        print("Count decremented")
    
    else:
        print("Unknown event")


@app.get("/")
async def get():
    with open('./static/index.html') as fh:
        data = fh.read()
    return Response(content=data, media_type="text/html")



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Data received - {data}")
        await message_handler(data, websocket)
        # await websocket.send_text(f"Message text was: {data}")

