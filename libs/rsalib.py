import random
import string
from SecureHTTP import generate_rsa_keys
from db.session import redis_session

from SecureHTTP import generate_rsa_keys
from SecureHTTP import AESEncrypt

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
    (pubkey, privkey) = generate_rsa_keys(incall=True)
    aeskey = makeAesKey()
    pubkey = AESEncrypt(aeskey, str(pubkey, encoding="utf-8"))
    redis_session().mset({
        "pubkey": pubkey,
        "privkey": privkey,
        "aeskey": aeskey
    })