import responder
from starlette.websockets import WebSocket, WebSocketDisconnect
from typing import Dict
import asyncio
from threading import Thread, Lock
from queue import Queue, Empty, Full


class WebSocketServer(object):
    def __init__(self, *, address: str = '0.0.0.0', port: int = 8080, location: str = '/'):
        self.address = address
        self.port = port
        self.location = location

        self.clients: Dict[str, WebSocket] = {}
        self.locker = Lock()

        self.elo = asyncio.get_event_loop()  # Eventloop Object
        self.bcPutTimeoutSecs = 5
        self.bcGetTimeoutSecs = 5
        self.bcCounter = 0
        self.bcQueue = Queue()  # Queue for message
        self.bcThread = Thread(target=self._bcWatcher, daemon=True)
        self.bcThread.start()

        self.api = responder.API()
        self.api.add_route(route=self.location, endpoint=self.wsSession, websocket=True)

        self.api.run(address=self.address, port=self.port)

    async def wsSession(self, ws: WebSocket):
        await ws.accept()
        key = ws.headers['sec-websocket-key']
        with self.locker:
            if key not in self.clients.keys():
                self.clients[key] = ws
        while True:
            try:
                message = await ws.receive_text()
            except (WebSocketDisconnect,) as e:
                break
            else:
                for k, v in self.clients.items():
                    if k != key:
                        await v.send_text(data=message)  # no exception ???

        with self.locker:
            if key in self.clients.keys():
                del self.clients[key]
        await ws.close()

    async def _onAir(self, *, message: str) -> None:
        with self.locker:
            for k, v in self.clients.items():
                await v.send_text(data=message)

    def _bcWatcher(self):
        while True:
            try:
                message = self.bcQueue.get(timeout=self.bcGetTimeoutSecs)
            except (Empty,) as e:
                self.broadCast(message='Queue is empty!')  # for debug
            else:
                self.elo.run_until_complete(future=self._onAir(message=message))
                self.bcCounter += 1

    # ---------------------------------------------------------------------------------
    def broadCast(self, *, message: str):
        try:
            self.bcQueue.put(item=message, timeout=self.bcPutTimeoutSecs)
        except (Full,) as e:
            print(e)
            pass
    # ---------------------------------------------------------------------------------


if __name__ == '__main__':
    def main():
        S = WebSocketServer()
        pass


    main()
