# Do something here
from fastapi import FastAPI, WebSocket, Response
import uvicorn

api_app = FastAPI()

class FastUI:

    @api_app.get("/")
    async def something(self):
        with open("./static/index.html") as fh:
            data = fh.read()
        return Response(content=data, media_type="text/html")
    

    @api_app.websocket("/ws")
    async def websocket_endpoint(self, websocket: WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            print(f"Data received - {data}")
            await self.message_handler(data, websocket)
            # await websocket.send_text(f"Message text was: {data}")
    
    async def message_handler(self, data, websocket):
        print(f"Message Handler - {data}")
        # from pprint import pprint
        # pprint(self.store)
        # if data == 'i':
        #     self.store["count"] += 1
        #     await websocket.send_text(str(store["count"]))
        #     print("Count incremented")

        # elif data == 'd':
        #     self.store["count"] -= 1
        #     await websocket.send_text(str(store["count"]))
        #     print("Count decremented")
        
        # else:
        #     print("Unknown event")




class Store(dict):
    
    def __setitem__(self, __key, __value) -> None:
        # Update the key as usual
        super().__setitem__(__key, __value)
        
        # TODO Send out an update via websocket



def run(fastui_app):
    uvicorn.run(api_app, host="127.0.0.1", port=8000)
