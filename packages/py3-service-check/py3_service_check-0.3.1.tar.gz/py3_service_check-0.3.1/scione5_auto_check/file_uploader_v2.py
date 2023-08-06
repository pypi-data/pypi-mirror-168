#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/1 4:35 下午
# @Author  : Meng Wang
# @Site    : 
# @File    : file_uploader.py
# @Software: PyCharm

# 引入MinIO包。
from minio import Minio

# Example anonymous read-write bucket policy.
R_W_POLICY_FORMAT = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
            ],
            "Resource": "arn:aws:s3:::%s",
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListMultipartUploadParts",
                "s3:AbortMultipartUpload",
            ],
            "Resource": "arn:aws:s3:::%s/*",
        },
    ],
}

"""
client.set_bucket_policy("my-bucket", json.dumps(policy))
"""


def upload(endpoint, file_path, prefix, filename, bucket='scione5'):
    try:
        # 使用endpoint、access key和secret key来初始化minioClient对象。
        minioClient = Minio(endpoint=endpoint,
                            access_key='AyW7vxcBsyc1DnhJ',
                            secret_key='0BVHeFE0kL65HRCp',
                            secure=False)
        if not minioClient.bucket_exists(bucket_name=bucket):
            # 创建bucket
            minioClient.make_bucket(bucket_name=bucket)
            minioClient.set_bucket_policy(bucket_name=bucket, policy=R_W_POLICY_FORMAT % (bucket, bucket))
        minioClient.fput_object(bucket, prefix + "/" + filename, file_path)
        return "http://" + endpoint + "/" + bucket + "/" + prefix + "/" + filename
    except Exception as e:
        print(e)
        print("上传失败")


if __name__ == '__main__':
    print(upload(endpoint="192.168.100.102:9000", file_path="./logo.png", prefix="sale", filename="tyyeysd.png", bucket="pt100"))