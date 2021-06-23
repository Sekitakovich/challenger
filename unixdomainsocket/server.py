import socketserver
import socket
from loguru import logger

HOST, PORT = "", 12345


class SampleHandler(socketserver.BaseRequestHandler, object):
    def handle(self):
        client = self.request
        address = self.client_address[0]
        logger.info(self.request)


class Receiver(socketserver.ThreadingTCPServer, object):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


class Main(object):
    def __init__(self):
        self.receiver = Receiver((HOST, PORT), SampleHandler)
        self.receiver.serve_forever()


if __name__ == "__main__":
    def main():
        M = Main()

        pass

    main()

