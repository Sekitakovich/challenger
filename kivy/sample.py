from kivy.app import App

import responder
from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect  # 毎回これを忘れて探す

import time
from threading import Thread
from typing import Dict
from loguru import logger


class SampleAPP(App):  # associated with sample.kv

    def __init__(self):
        super().__init__()
        self.active: bool = True
        self.counter: int = 0

        self.loop: Thread = Thread(target=self.cycle, name='loop', daemon=True)
        self.loop.start()

    def cycle(self):
        while self.active:
            logger.debug(self.counter)
            self.counter += 1
            time.sleep(1)

    def on_start(self):
        logger.debug("App Start!!")

    def on_stop(self):
        self.active = False
        logger.debug("App End!!")


class Main(object):

    def __init__(self):

        self.debug: bool = True

        self.guiStage = SampleAPP()
        self.kivyThread = Thread(target=self.kivyStart, daemon=True)
        self.kivyThread.start()

        self.clients: Dict[str, any] = {}
        self.api = responder.API(debug=True)
        self.api.add_route('/ws', self.wsserver, websocket=True)
        self.api.run(address='0.0.0.0', port=80)

    def kivyStart(self):
        self.guiStage.run()

    async def wsserver(self, ws: WebSocket):

        await ws.accept()
        key = ws.headers.get('sec-websocket-key')
        self.clients[key] = ws
        logger.debug('+++ Websocket: hold %d clients' % (len(self.clients)))
        if self.debug:
            logger.debug('%s has come' % key)

        while True:
            try:
                msg = await ws.receive_text()
            except WebSocketDisconnect as e:
                del self.clients[key]
                await ws.close()
                if self.debug:
                    logger.debug(e, '%s was gone' % key)
                break
            else:
                for k, v in self.clients.items():
                    if k != key:
                        await v.send_text(msg)
                if self.debug:
                    logger.debug('[%s] from %s' % (msg, key))


if __name__ == "__main__":
    main = Main()
    # KivyGUI().run()
