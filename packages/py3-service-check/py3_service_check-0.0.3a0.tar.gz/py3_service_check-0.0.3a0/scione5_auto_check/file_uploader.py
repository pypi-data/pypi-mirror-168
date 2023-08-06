#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 4:35 下午
# @Author  : Meng Wang
# @Site    : 
# @File    : file_uploader.py
# @Software: PyCharm

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json


def upload_file(access_token, org_id, upload_url):
    multipart_data = MultipartEncoder(
        fields={
            # a file upload field
            'file': ("logo.png", open('logo.png', 'rb'), 'text/plain'),
            # plain text fields
            'orgId': str(org_id),
            'type': "room"
        }
    )

    headers = {
        "Authorization": "Bearer " + access_token,
        'Content-Type': multipart_data.content_type
    }
    try:
        response = requests.post(upload_url, data=multipart_data,
                                 headers=headers, timeout=15).text
        res_dict = json.loads(response)
        if res_dict["success"]:
            #上传成功
            return res_dict["data"]["downAddress"]

        return None
    except Exception as e:
        return None
