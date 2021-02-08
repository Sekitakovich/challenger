import responder
from loguru import logger

from useResponder.common import Responder


class Admin(object):

    def on_get(self, req: responder.Request, res: responder.Response, *, mode: str = ''):
        res.content = Responder.api.template('admin.html', title='Welcome', mode=mode)

    async def on_post(self, req: responder.Request, res: responder.Response, *, mode: str = ''):
        if mode == 'save':
            pass
        # res.content = Responder.api.template('admin.html', title='Welcome', message=message, mode=mode)
