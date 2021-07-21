import json,time
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.datastructures import MutableHeaders
from SecureHTTP import RSADecrypt,AESDecrypt,AESEncrypt

from db.session import redis_session
from libs.snowflakeAlgorithm import IdWorker
from core.config import settings
worker = IdWorker(1, 2, 0)


class MessageSecureHTTPMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            responder = _MessageSecureHTTPResponder(self.app)
            await responder(scope, receive, send)
            return
        await self.app(scope, receive, send)

class _MessageSecureHTTPResponder:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.receive: Receive = unattached_receive
        self.send: Send = unattached_send
        self.url = ''
        self.initial_message: Message = {}
        self.started = False
        self.privkey = redis_session().get('privkey')
        self.asekey = ''

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive)
        self.url = request.url.path
        self.receive = receive
        self.send = send
        await self.app(scope, self.receive_with_msg, self.send_with_msg)

    async def receive_with_msg(self) -> Message:
        '''
            解密返回
        '''
        message = await self.receive()

        if self.url not in settings.EXURL:
            return message


        body = json.loads(str(message['body'], encoding="utf-8"))
        self.asekey = RSADecrypt(self.privkey,body['key'])
        body = AESDecrypt(self.asekey,body['value'])

        message['body'] = bytes(json.dumps(body), encoding='utf-8')
        return message

    async def send_with_msg(self, message: Message) -> None:
        '''
            加密返回
        '''
        if self.url not in settings.EXURL:
            await self.send(message)
            return

        if message["type"] == "http.response.start":
            self.initial_message = message
            return

        elif message["type"] == "http.response.body":
            headers = MutableHeaders(raw=self.initial_message['headers'])

            # bytes to dict => dict to bytes
            body = json.loads(str(message['body'], encoding="utf-8"))
            body = dict(data=AESEncrypt(self.asekey, json.dumps(body, separators=(',', ':')), output_type="str"))
            body = bytes(json.dumps(body), encoding='utf-8')

            # 更新 body
            message["body"] = body

            # 自定义响应header
            headers["Content-Length"] = str(len(body))
            headers['timestamp'] = round(time.time())
            headers['nonce'] = worker.get_id()

            self.initial_message['headers'] = headers._list
            await self.send(self.initial_message)

            await self.send(message)


async def unattached_receive() -> Message:
    raise RuntimeError("receive awaitable not set")  # pragma: no cover


async def unattached_send(message: Message) -> None:
    raise RuntimeError("send awaitable not set")  # pragma: no cover
