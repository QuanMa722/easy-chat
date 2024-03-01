
# -*- coding: utf-8 -*-

# 导入需要的第三方库
import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib
import re


class RequestApi(object):
    def __init__(self, upload_file_path):
        self.appid = ""
        self.secret_key = ""
        self.lfasr_host = 'https://raasr.xfyun.cn/v2/api'
        self.api_upload = '/upload'
        self.api_get_result = '/getResult'
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()


    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa


    def upload(self):

        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"

        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url = self.lfasr_host + self.api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)

        result = json.loads(response.text)

        return result


    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"

        try:
            status = 3
            # 建议使用回调的方式查询结果，查询接口有请求频率限制
            while status == 3:
                response = requests.post(url=self.lfasr_host + self.api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                         headers={"Content-type": "application/json"})
                # print("get_result_url:",response.request.url)
                result = json.loads(response.text)

                status = result['content']['orderInfo']['status']
                print("Please wait.")
                if status == 4:
                    break

            order_result = json.loads(result['content']['orderResult'])
            lattice = order_result['lattice']
            chinese_text = ""

            for item in lattice:
                json_1best = item.get('json_1best', '')
                chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
                chinese_chars = chinese_pattern.findall(json_1best)
                chinese_text += " ".join(chinese_chars) + " "

            text = chinese_text.replace(" ", '')
            # print("Speak:" + text)
            return text
        except Exception as e:
            print(f"An error occurred: {e}")




