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