from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.datastructures import Headers, MutableHeaders
# https://github.com/jackerzz/Python-SecureHTTP
# https://github.com/florimondmanca/msgpack-asgi/blob/master/src/msgpack_asgi/_middleware.py
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
        self.should_decode_from_msgpack_to_json = False
        self.should_encode_from_json_to_msgpack = False
        self.receive: Receive = unattached_receive
        self.send: Send = unattached_send
        self.initial_message: Message = {}
        self.started = False

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # message = await self.receive()
        await self.app(scope, self.receive_with_msg, self.send_with_msg)

    async def receive_with_msg(self) -> Message:
        message = await self.receive()
        
        print("receive_with_msg",message)
        return message

    async def send_with_msg(self, message: Message) -> None:
        print("send_with_msg",message)
        assert self.should_encode_from_json_to_msgpack
        # self.initial_message = message
        # if message["type"] == "http.response.start":
        #     await self.send(message)
        #     return
        # else:
        #     headers = MutableHeaders(raw=self.initial_message["headers"])
        #     headers["Content-Type"] = "application/x-msgpack"
        #     body = message.get("body", b"")
        #     headers["Content-Length"] = str(len(body))
        #     message["body"] = body
        await self.send(message)
            
async def unattached_receive() -> Message:
    raise RuntimeError("receive awaitable not set")  # pragma: no cover


async def unattached_send(message: Message) -> None:
    raise RuntimeError("send awaitable not set")  # pragma: no cover