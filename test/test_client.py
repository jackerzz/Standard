# -*- coding: utf-8 -*-
import json
import requests
from SecureHTTP import EncryptedCommunicationClient,AESDecrypt
from db.session import redis_session
def test_client():
    clisnt = redis_session()
    pubkey = clisnt.get('pubkey')
    aeskey = clisnt.get("aeskey")
    pubkey = AESDecrypt(aeskey,pubkey)


    post = {"name": "sbfsdafsdafdsafsdafsdafsda", "txet": "hhhhhhh"}
    ec = EncryptedCommunicationClient(pubkey)
    encryptedPost = ec.clientEncrypt(post)
    encryptedPost['key'] = str(encryptedPost['key'],encoding='utf-8')
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/json',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
    }
    resp = requests.post("http://127.0.0.1:8000/api/v1/rbac/dataset1/protected", json=encryptedPost,headers=headers).json()
    resp = ec.clientDecrypt(resp)
    print("\n服务端返回数据：%s" %resp)
    
'''
$ time pytest test/test_client.py -s
=============================================== test session starts ===============================================
platform win32 -- Python 3.7.6, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: E:\HexoProject\Standard
collecting ... 2021-07-07 14:28:14.590 | DEBUG    | core.config:get_config:86 - 识别开发者模式
2021-07-07 14:28:14.590 | DEBUG    | core.config:get_config:98 - 项目配置加载完成
collected 1 item                                                                                                   

test\test_client.py
服务端返回数据：{'name': 'sbfsdafsdafdsafsdafsdafsda', 'txet': 'hhhhhhh'}
========================================== 1 passed, 1 warning in 1.13s ===========================================
real    0m2.062s
user    0m0.000s
sys     0m0.046s
'''