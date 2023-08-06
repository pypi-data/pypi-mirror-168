import hashlib
import hmac
import base64
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from urllib import request, parse, error
import ssl
import simplejson
import json

s_time = 2 * 60 * 60 * 1000
l_time = 30 * 24 * 60 * 60 * 1000

sk = 'knoczslufdasvhbivbewnrvuywachsrawqdpzesccknrhhetgmrcwfqfudywbeon'
pubkey = b'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAokFjy0wLMKH0/39hxPN6JYRkMDXzvVIGQh55Keo2LIsP/jRU/yZHT/Vkg34yU9koNjSaacPvooXEoI5eFGuRrsBMrotZ5xfejCrTbGvZqjhnMPBheDmxfflIZzRrF/zoQvF0nIbmGNkxEfROHtDDkgNuGRdthXrNavCgfM2z3LNF83UT9CGpxJWBeKK3pXfYLsQ4f8uyrQRcy2BhKfJ/PKai1mocXYqr07JfQ0XZM4xIzuQ7E4ybNk5IFreDuuhF63wXAi1uonGzqjEYcbC1xT2boNiZORoOQWpAHhSbIRpljmW/uHBvoKZ573PQbbxE62hXv1Z1iVky0dtAV65dXwIDAQAB'

ssl._create_default_https_context = ssl._create_unverified_context


def __pin(key, secret):
    app_config = [key.split("-")[1], secret.split("-")[1]]
    tmp = ''.join(app_config)
    return str(int(tmp, 16)).zfill(9)[:6]


def __token(pm, short_expire_time, long_expire_time):
    e_data = pm + str(int(round(time.time() * 1000)) + short_expire_time)
    r_data = pm + str(int(round(time.time() * 1000)) + long_expire_time)

    security = list()
    security.append(hmac.new(sk.encode('UTF-8'), e_data.encode('UTF-8'), hashlib.sha256).hexdigest())
    security.append(hmac.new(sk.encode('UTF-8'), r_data.encode('UTF-8'), hashlib.sha256).hexdigest())

    return security


def __token2(pm, short_expire_time):
    e_data = pm + str(int(round(time.time() * 1000)) + short_expire_time)

    return hmac.new(sk.encode('UTF-8'), e_data.encode('UTF-8'), hashlib.sha256).hexdigest()


def __accesstoken(pm, key, secret, accesstoken, refreshtoken):
    data_encryption = pm + '$' + key + '$' + secret + '$' + accesstoken + '$' + refreshtoken
    keyder = base64.b64decode(pubkey)
    rsa_key = RSA.importKey(keyder)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    x = cipher_rsa.encrypt(data_encryption.encode('UTF-8'))
    return base64.b64encode(x).decode()


def urlopen(key, secret, url, data=None, headers=None, method=None, timeout=None):
    if headers is None:
        headers = {}
    pin = __pin(key, secret)
    security = __token(pin, s_time, l_time)
    accesstoken = __accesstoken(pin, key, secret, security[0], security[1])

    if data is not None:
        data = json.dumps(data)
        data = bytes(data, 'UTF-8')

    req = request.Request(url, data)

    if method is not None:
        req.method = method

    if not timeout:
        timeout = object()

    req.add_header('apim-accesstoken', accesstoken)
    req.add_header('Content-Type', 'application/json;charset=utf-8')
    req.add_header('User-Agent', 'Python_enos_api')

    for key, value in headers.items():
        req.add_header(key, value)

    try:
        response = request.urlopen(req, timeout=timeout)

        content = response.read().decode('UTF-8')
        try:
            content_json = simplejson.loads(content)
        except:
            return content

        try:
            apim_status = content_json['apim_status']

            if apim_status == 4011:
                apim_refreshtoken = content_json['apim_refreshtoken']
                token = __token2(pin, s_time)
                accesstoken = __accesstoken(pin, key, secret, token, apim_refreshtoken)
            elif apim_status == 4012:
                security = __token(pin, s_time, l_time)
                accesstoken = __accesstoken(pin, key, secret, security[0], security[1])
            else:
                return content_json

            print('the second time request')

            if data is not None:
                data = json.dumps(data)
                data = bytes(data, 'UTF-8')

            req = request.Request(url, data)
            req.add_header('apim-accesstoken', accesstoken)
            req.add_header('Content-Type', 'application/json;charset=utf-8')
            req.add_header('User-Agent', 'Python_enos_api')

            for key, value in headers.items():
                req.add_header(key, value)

            response = request.urlopen(req)
            return response.read().decode('UTF-8')
        except:
            return content_json
    except error.URLError as err:
        print(err)
