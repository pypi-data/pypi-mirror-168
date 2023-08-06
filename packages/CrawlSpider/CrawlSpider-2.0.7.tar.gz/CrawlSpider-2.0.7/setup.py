# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2021/1/21 18:15
# __fileName__ : GoldenCoordinateV2 setup.py.py
# __devIDE__ : PyCharm

from setuptools import setup, find_packages
import os
import sys



requires = [
    'pyperclip==1.8.2',
    'PySide2==5.15.2',
    'PySocks==1.7.1',
    'PyYAML==5.4.1',
    'PyExecJS==1.5.1',
    'protobuf==3.14.0',
    'pkginfo==1.8.3',
    'cos-python-sdk-v5==1.9.15',
    'requests==2.26.0',
    'beautifulsoup4==4.10.0',
    'lxml==4.6.3',
    'DBUtils==3.0.2',
    'PyMySQL==0.9.3',
    'selenium==4.0.0',
    'aiofiles==0.8.0',
    'aiohttp==3.8.1',
    'aiohttp-requests==0.1.3',
    'fake-useragent==0.1.11',
    'retrying==1.3.3',
    'redis==4.3.3',
    'aiomysql==0.0.22',
    'fire==0.4.0',
    'psutil==5.9.1',
    'urllib3==1.26.6',
    'boto3==1.24.24',
    'botocore==1.27.24',
    'aliyun-python-sdk-core-v3==2.13.33',
    'aliyun-python-sdk-green==3.6.5',
    'aliyun-python-sdk-kms==2.15.0',
    'tenacity==8.0.1',
    "psycopg2-binary",
    "psycopg",
    "pytz",
    "pyyaml==5.4.1",
    "pyexcel_xlsx==0.6.0",
    "loguru==0.6.0"
]

# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open("__version__.py", "r", encoding="utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(

    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    keywords='spider scrapy beatifulsoup xpath 正则',
    project_urls={
        'Author Website': 'https://blog.csdn.net/qq_36154755',
    },
    include_package_data=True,
    packages=find_packages(),
    install_requires=requires,
    python_requires='>=3.6',
    extras_require={
        "asyncLoop": [
            'uvloop'
        ],
        "build": [
            "twine"
        ]
    },
    entry_points={
        'console_scripts': [
            'CrawlSpiderUtils = CrawlSpider.Utils.__main__:main'
        ]
    }
)

# python CrawlSpider/Utils/twineUtils.py build --username=None --password=None --version=None --is_publish=False





