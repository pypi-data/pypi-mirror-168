#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/26 10:24 上午
# @Author  : Meng Wang
# @Site    :
# @File    : scione5_encrypt.py
# @Software: PyCharm
import base64
import execjs
from urllib import parse

"""
需要执行的js代码
"""
JSCode = r'''
    function encryptContent(text) {
    const AuthTokenKey = '79c2965a4c113d89' //AES密钥
    const base64 = getSecret(AuthTokenKey)
    const ciphertext = encrypt(text, base64).toString()
    return ciphertext
  }
   
 function  getSecret(str) {
    let str_s = str
    let encodeData = window.btoa(encodeURIComponent(str))
    while (encodeData.length < 16) {
      str_s += '_'
      encodeData = window.btoa(encodeURIComponent(str_s))
    }
    return encodeData.slice(encodeData.length - 16, encodeData.length)
  }
 function encrypt(content, key) {
    let sKey = CryptoJS.enc.Utf8.parse(key)
    let sContent = CryptoJS.enc.Utf8.parse(content)
    let encrypted = CryptoJS.AES.encrypt(sContent, sKey, {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7,
    })
    return encrypted.toString()
  }
'''

from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import base64


class PrpCrypt(object):

    def __init__(self):
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def aes_cipher(self, key, aes_str):
        # 使用key,选择加密方式
        aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        pad_pkcs7 = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')  # 选择pkcs7补全
        encrypt_aes = aes.encrypt(pad_pkcs7)
        # 加密结果
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 解码
        encrypted_text_str = encrypted_text.replace("\n", "")
        # 此处我的输出结果老有换行符，所以用了临时方法将它剔除

        return encrypted_text_str

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, key, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        msg = aes.decrypt(res).decode("utf8")
        return self.unpad(msg)

if __name__ == '__main__':
    AuthTokenKey = '79c2965a4c113d89'
    str_s = AuthTokenKey
    encodedKey = base64.encodebytes(parse.quote(AuthTokenKey).encode("utf-8"))
    while len(encodedKey) < 16:
        str_s += '_'
        encodedKey = base64.encodebytes(parse.quote(str_s).encode("utf-8"))

    encodedKey_str = str(encodedKey, "utf-8")

    encodedKey_str_real = encodedKey_str[len(encodedKey_str) - 16:]

    encryption_result = PrpCrypt().aes_cipher(encodedKey_str_real, "a-123456")

    print(encryption_result)
