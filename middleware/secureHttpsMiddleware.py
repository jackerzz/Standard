import json
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.datastructures import MutableHeaders
from SecureHTTP import EncryptedCommunicationServer
from db.session import redis_session


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
        self.headers = ''
        self.method = str
        self.initial_message: Message = {}
        self.started = False
        self.client = redis_session()
        self.resServer = EncryptedCommunicationServer(
            self.client.get('privkey'))

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.headers = MutableHeaders(scope=scope)
        request = Request(scope, receive)
        self.url = request.url.path
        self.method = scope["method"]
        self.receive = receive
        self.send = send
        await self.app(scope, self.receive_with_msg, self.send_with_msg)

    async def receive_with_msg(self) -> Message:
        '''
            解密返回
        '''
        message = await self.receive()
        print("解密返回原生message:", message)
        body = json.loads(str(message['body'], encoding="utf-8"))
        body = self.resServer.serverDecrypt(body)
        message['body'] = bytes(json.dumps(body), encoding='utf-8')
        print('解密成功message：', message)
        return message

    async def send_with_msg(self, message: Message) -> None:
        '''
            加密返回
        '''
        if self.url in ['/docs', '/api/v1/openapi.json']:
            await self.send(message)
            return

        if message["type"] == "http.response.start":
            self.initial_message = message
            # await self.send(message)
            return

        elif message["type"] == "http.response.body":
            print("加密返回原生http.response.body --> message:", message)
            print("加密返回原生http.response.start --> message:", self.initial_message)
            headers = MutableHeaders(raw=self.initial_message['headers'])
            # bytes to dict => dict to bytes
            body = json.loads(str(message['body'], encoding="utf-8"))
            body = self.resServer.serverEncrypt(body)
            body = bytes(json.dumps(body), encoding='utf-8')

            # 更新 body
            message["body"] = body
            print("更新 body ", body)

            # 自定义响应header
            headers["Content-Length"] = str(len(body))
            headers['ac'] = "hhhh"
            headers.append("Set-Cookie", "fasdfdsa")

            self.initial_message['headers'] = headers._list
            await self.send(self.initial_message)

            await self.send(message)


async def unattached_receive() -> Message:
    raise RuntimeError("receive awaitable not set")  # pragma: no cover


async def unattached_send(message: Message) -> None:
    raise RuntimeError("send awaitable not set")  # pragma: no cover
