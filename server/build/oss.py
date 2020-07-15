# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import json
import base64
import time
import datetime
import hmac
from hashlib import sha1 as sha
import os

# 请填写您的AccessKeyId
access_key_id = os.getenv('ACCESS_KEY_ID', '')
# 请填写您的AccessKeySecret
access_key_secret = os.getenv('ACCESS_KEY_SECRET', '')
# host的格式为 bucketname.endpoint ，请替换为您的真实信息。
host = os.getenv('HOST', '')
# callback_url为 上传回调服务器的URL，请将下面的IP和Port配置为您自己的真实信息。
callback_url = os.getenv('CALLBACK_URL', '')
# 用户上传文件时指定的前缀。
expire_time = int(os.getenv('EXPIRE_TIME', 60))
upload_dir = os.getenv('UPLOAD_DIR', '')

def get_iso_8601(expire):
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        now = int(time.time())
        expire_syncpoint = int(now + expire_time)
        expire = get_iso_8601(expire_syncpoint)
        policy_dict = {}
        policy_dict['expiration'] = expire
        condition_array = []
        array_item = []
        array_item.append('starts-with')
        array_item.append('$key')
        array_item.append(upload_dir)
        condition_array.append(array_item)
        policy_dict['conditions'] = condition_array
        policy = json.dumps(policy_dict).strip()
        policy_encode = base64.b64encode(policy.encode())
        h = hmac.new(access_key_secret.encode(), policy_encode, sha)
        sign_result = base64.encodebytes(h.digest()).strip()

        callback_dict = {}
        callback_dict['callbackUrl'] = callback_url
        callback_dict['callbackBody'] = 'filename=${object}&size=${size}&mimeType=${mimeType}' \
                                        '&height=${imageInfo.height}&width=${imageInfo.width}'
        callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded'
        callback_param = json.dumps(callback_dict).strip()
        base64_callback_body = base64.b64encode(callback_param.encode())

        token_dict = {}
        token_dict['accessid'] = access_key_id
        token_dict['host'] = host
        token_dict['policy'] = policy_encode.decode()
        token_dict['signature'] = sign_result.decode()
        token_dict['expire'] = expire_syncpoint
        token_dict['dir'] = upload_dir
        token_dict['callback'] = base64_callback_body.decode()
        result = json.dumps(token_dict)
        self.write(result)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
