import responder
from loguru import logger

from useResponder.common import Responder
from useResponder.admin import Admin


class Main(object):

    def __init__(self):
        self.address = '0.0.0.0'
        self.port = 80

        Responder.api.add_route(route='/', endpoint=self.topPage)
        Responder.api.add_route(route='/maps', endpoint=self.maps)
        Responder.api.add_route(route='/{mode}', endpoint=Admin)

    def start(self):
        Responder.api.run(address=self.address, port=self.port)

    def topPage(self, req: responder.Request, res: responder.Response):
        res.content = Responder.api.template('index.html', title='Top')

    def maps(self, req: responder.Request, res: responder.Response):
        res.content = Responder.api.template('maps.html', title='Top')

if __name__ == '__main__':
    def main():
        M = Main()
        M.start()
        pass


    main()
