import json
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.datastructures import MutableHeaders
from libs.rsalib import RsaServer
class MessageSecureHTTPMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            responder = _MessageSecureHTTPResponder(self.app)
            await responder(scope, receive, send)
            return
        await self.app(scope, receive, send)


# https://github.com/florimondmanca/msgpack-asgi/blob/master/src/msgpack_asgi/_middleware.py
class _MessageSecureHTTPResponder:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.receive: Receive = unattached_receive
        self.send: Send = unattached_send
        self.url = ''
        self.headers = ''
        self.method = str
        self.initial_message: Message = {}
        self.started = False
        self.resServer = RsaServer()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.headers = MutableHeaders(scope=scope)
        request = Request(scope, receive)
        self.url = request.url.path
        self.method = scope["method"]
        self.receive = receive
        self.send = send
        await self.app(scope, self.receive_with_msg, self.send_with_msg)

    async def receive_with_msg(self) -> Message:
        message = await self.receive()
        # 解密数据
        print(message)
        body = json.loads(message['body'])
        # body 解密数据
        body = self.resServer.rsaServerDecrypt(body)
        message = json.dumps(body)
        return message

    async def send_with_msg(self, message: Message) -> None:
        if self.url in ['/docs','/api/v1/openapi.json']:
            await self.send(message)
            return

        if message["type"] == "http.response.start":
            self.initial_message = message
            await self.send(message)
            return

        elif message["type"] == "http.response.body":
            headers = MutableHeaders(raw=self.initial_message['headers'])
            body = json.loads(message['body'])
            # body 进行对称加密
            print(body)
            body = await self.resServer.rsaServerEncrypt(body)
            print(body)
            body = json.dumps(body)

            # 定义 响应header
            headers["Content-Type"] = "application/json"
            headers["Content-Length"] = str(len(body))
            headers['type'] = "http.response.body"
            message["body"] = body
            headers['ac'] = "hhhh"
            header_value = "{}={};".format(
                headers['ac'],
                "jacdsafdsaf",
            )
            headers.append("Set-Cookie", header_value)
            await self.send(headers)
            await self.send(message)


async def unattached_receive() -> Message:
    raise RuntimeError("receive awaitable not set")  # pragma: no cover


async def unattached_send(message: Message) -> None:
    raise RuntimeError("send awaitable not set")  # pragma: no cover
