# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osscore']

package_data = \
{'': ['*']}

install_requires = \
['aliyun-python-sdk-core>=2.13.36,<3.0.0',
 'aliyun-python-sdk-sts>=3.1.0,<4.0.0',
 'oss2>=2.16.0,<3.0.0']

setup_kwargs = {
    'name': 'osscore',
    'version': '0.1.1',
    'description': '',
    'long_description': '## 易于使用，人性化的阿里云oss工具包\n\n### 安装\n\n```bash\npip install osscore\n```\n\n### 使用\n\n#### OSSFileSystem\n\n- access_key_id or define env OSS_ACCESS_KEY_ID\n- access_key_secret or define env OSS_ACCESS_KEY_SECRET\n- endpoint or define env OSS_ENDPOINT\n- token\n\n##### 上传文件\n\n```python\nfrom osscore import OSSFileSystem\n\nOSSFileSystem().upload("bucket_name", "local_path", "key")\n```\n\n##### 下载文件\n\n> local_path 不写会返回 temp file\n\n```python\nfrom osscore import OSSFileSystem\n\nOSSFileSystem().download("bucket_name", "key", "local_path")\n```',
    'author': 'similarface',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
