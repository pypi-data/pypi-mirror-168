# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tencentcos_storage']

package_data = \
{'': ['*']}

install_requires = \
['cos-python-sdk-v5>=1.9.4,<2.0.0']

setup_kwargs = {
    'name': 'django-cos-storage',
    'version': '0.3.0',
    'description': 'A django app for Tencent Cloud Object Storage. 腾讯云对象存储（COS）服务 for Django。',
    'long_description': '# Django TencentCOS Storage\n\n腾讯云对象存储（COS）服务 for Django。\n\n## 环境要求\n\nPython: >=3.7, <4\n\nDjango: >=2.2, <3.3\n\n## 安装\n\n```\npip install django-tencentcos-storage\n```\n\n## 基本使用\n\n在项目的 settings.py 中设置 `DEFAULT_FILE_STORAGE`：\n\n```python\nDEFAULT_FILE_STORAGE = "tencentcos_storage.TencentCOSStorage"\n```\n\n此外，还需要设置腾讯云对象存储服务相关的必要信息：\n\n```python\nTENCENTCOS_STORAGE = {\n    "BUCKET": "存储桶名称",\n    "CONFIG": {\n        "Region": "地域信息",\n        "SecretId": "密钥 SecretId",\n        "SecretKey": "密钥 SecretKey",\n    }\n}\n```\n\n详情可参考 [腾讯云对象存储官方文档](https://cloud.tencent.com/document/product/436)\n\n## 设置\n\n### 示例\n```python\nTENCENTCOS_STORAGE = {\n    # 存储桶名称，必填\n    "BUCKET": "存储桶名称",\n    # 存储桶文件根路径，选填，默认 \'/\'\n    "ROOT_PATH": "/",\n    # 上传文件时最大缓冲区大小（单位 MB），选填，默认 100\n    "UPLOAD_MAX_BUFFER_SIZE": 100,\n    # 上传文件时分块大小（单位 MB），选填，默认 10\n    "UPLOAD_PART_SIZE": 10,\n    # 上传并发上传时最大线程数，选填，默认 5\n    "UPLOAD_MAX_THREAD": 5,\n    # 腾讯云存储 Python SDK 的配置参数，详细说明请参考腾讯云官方文档\n    "CONFIG": {\n        "Region": "地域信息",\n        "SecretId": "密钥 SecretId",\n        "SecretKey": "密钥 SecretKey",\n    }\n}\n```\n\n### 说明\n\n**BUCKET**\n\n> 存储桶名称，必填\n\n**ROOT_PATH**\n> 文件根路径，选填，默认为 \'/\'\n\n**UPLOAD_MAX_BUFFER_SIZE**\n\n> 上传文件时最大缓冲区大小（单位 MB），选填，默认 100。\n> 其中缓冲区是一个线程安全队列，队列的元素为单个文件分块，队列中所有分块的大小加起来不超过 `UPLOAD_MAX_BUFFER_SIZE`。\n\n**UPLOAD_PART_SIZE**\n> 上传文件时分块大小（单位 MB），选填，默认 10。\n> `UPLOAD_MAX_BUFFER_SIZE` 和 `UPLOAD_PART_SIZE` 共同决定了缓冲队列的大小，即 `QueueSize` = `UPLOAD_MAX_BUFFER_SIZE` / `UPLOAD_PART_SIZE`。\n\n**UPLOAD_MAX_THREAD**\n\n> 并发上传的最大线程数，选填，默认 5。\n> 当文件的大小超过 `UPLOAD_PART_SIZE` 时将使用分块的方式并发上传文件，此配置项设置并发上传的最大线程数。如果文件大小不超过 `UPLOAD_PART_SIZE`，则不会使用分块的方式上传，此时该配置项不起任何作用。\n\n**CONFIG**\n> 腾讯云对象存储 Python SDK 的配置参数，其中 `Region`、`SecretId`、`SecretKey` 为必填参数。\n> \n> 关于配置参数的详细说明请参考 [腾讯云对象存储 Python SDK 官方文档](https://cloud.tencent.com/document/product/436/12269)\n\n',
    'author': 'deneon',
    'author_email': 'dtneon@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jukanntenn/django-tencentcos-storage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
