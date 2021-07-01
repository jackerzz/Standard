import random
import string
from SecureHTTP import generate_rsa_keys
from db.session import redis_session

from SecureHTTP import EncryptedCommunicationServer
from SecureHTTP import AESEncrypt, AESDecrypt

from db.session import redis_session


def makePassword(minlength=16, maxlength=25):
    '''
        生成随机密码或随机字符串
        # (16, 24, 32)
    '''
    length = random.randint(minlength, maxlength)
    letters = string.ascii_letters+string.digits
    letters = string.ascii_letters

    return ''.join([random.choice(letters) for _ in range(length)])

def makeAesKey(length=16):
    '''
        生成随机Aes 加密key 
        # AES 加密key 生成可选值长度： (16, 24, 32)
    '''
    letters = string.ascii_letters

    return ''.join([random.choice(letters) for _ in range(length)])

async def generateRsaKeySave():
    '''
        @generateRsaKeySave
        生成密钥对
        每隔一段时间会更新一次
    '''
    # https://aredis.readthedocs.io/en/latest/
    (pubkey, privkey) = generate_rsa_keys(incall=True)
    aeskey = makeAesKey()
    pubkey = AESEncrypt(aeskey, str(pubkey, encoding="utf-8"))
    await redis_session().mset({
        "pubkey": pubkey,
        "privkey": str(privkey, encoding="utf-8"),
        "aeskey": aeskey
    })

# https://github.com/jackerzz/Python-SecureHTTP
# https://github.com/jackerzz/Python-SecureHTTP/blob/master/examples/Demo/server.py
class RsaServer(object):
    def __init__(self) -> None:
        self.client = redis_session()
        self.sc = EncryptedCommunicationServer(self.client.get('privkey'))

    async def getPrivkey(self):
        '''
        获取私钥
        '''
        privkey = await self.client.get('privkey')
        return privkey

    async def rsaServerEncrypt(self, data):
        '''
           @rsaServerEncrypt
           服务端返回加密数据
        '''
        return self.sc.serverEncrypt(data)

    async def rsaServerDecrypt(self, data):
        '''
           @rsaServerDecrypt
           服务端解密数据
        '''
        return self.sc.serverDecrypt(data)
