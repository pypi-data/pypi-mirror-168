import datetime
import time
import hashlib
import os
import tempfile
import requests
import json
import zipfile
from urllib.parse import urlparse
from CrawlSpider.conf.settings import headers, uaDic
from PySide2 import QtCore as qtc
import yaml
from CrawlSpider.Utils.Settings import Settings


md5Crypt = qtc.QCryptographicHash(qtc.QCryptographicHash.Md5)

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
def bin2dec(string_num):
    return str(int(string_num, 2))
def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])
def bin2hex(string_num):
    return dec2hex(bin2dec(string_num))


def getRealUrl(detailUrl:str, listUrl:str):
    realUrl = detailUrl
    res = urlparse(detailUrl)
    if not res.netloc:
        if detailUrl.startswith('/'):
            result = urlparse(listUrl)
            realUrl = f"{result.scheme}://{result.netloc}{detailUrl}"
        elif detailUrl.startswith('.'):
            suffix = listUrl.split('/')[-1]
            prefix = listUrl.rstrip(suffix)
            realUrl = prefix + detailUrl
    if not res.scheme and detailUrl.startswith("//"):
        scheme = urlparse(listUrl).scheme
        realUrl = f'{scheme}:{detailUrl}'
    if not urlparse(realUrl).netloc:
        realUrl = getRealUrl('/' + realUrl, listUrl)
    return realUrl



def downloadFileFromInet(downloadedUrl, outputDir, outFile):
    resp = requests.get(downloadedUrl, headers = headers)
    status_code = 0
    retry = 3
    output = os.path.join(outputDir, outFile)
    while status_code != 200 and retry:
        status_code = resp.status_code
        if resp.status_code == 200:
            with open(output, 'wb') as fw:
                fw.write(resp.content)
            targetPath = os.path.join(outputDir, unzip(output, outputDir))
            if os.path.splitext(output)[-1] != os.path.splitext(targetPath)[-1]:
                os.remove(output)
            return targetPath
        else:
            print(f"下载 {downloadedUrl} 失败")
        retry -= 1


def md5_dict(item:dict, fields=['snapshotUrl', 'publish_time','title', 'source','author']):
    md5Crypt.reset()
    for field in fields:
        value = item[field]
        if value:
            md5Crypt.addData(value.encode())
    hash_string = bytes(md5Crypt.result().toHex()).decode('UTF-8')
    return hash_string

def md5_text(text:str,salt="12345"):
    md5 = hashlib.md5(salt.encode())
    md5.update(text.encode())
    return md5.hexdigest()

def initDateTime(period=None, days=1):
    tds = []

    if period:
        try:
            start_time = datetime.datetime.strptime(period[0], '%Y-%m-%d')
            end_time = datetime.datetime.strptime(period[1], '%Y-%m-%d')
            for day in range((end_time - start_time).days + 1):
                td = (start_time + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
                ttd = (start_time + datetime.timedelta(days=day + 1)).strftime('%Y-%m-%d')
                print(td, ttd)
                tds.append(td)
        except Exception as e:
            print(e)

    elif days:
        if isinstance(days, int):
            yd = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
            td = (datetime.datetime.now() - datetime.timedelta(days=days - 1)).strftime('%Y-%m-%d')
            print(yd, td)
            tds.append(yd)

    else:
        print('时间参数设置错误')

    return tds





def getOrigin():
    url = 'http://httpbin.org/get'
    res = requests.get(url).json()
    print(res)
    return res.get('origin')

def initUaCache(uaFile=None, version='0.1.11', **kwargs):
    uaFile = uaFile or ''
    DB = os.path.join(
        tempfile.gettempdir(),
        'fake_useragent_{version}.json'.format(
            version=version,
        )
    )
    print(DB)
    if not os.path.exists(DB):
        if uaFile and os.path.isfile(uaFile) and os.path.exists(uaFile):
            with open(uaFile, 'rb') as fr, open(DB, 'wb') as fw:
                fw.write(fr.read())
        elif kwargs.get('url'):
            url = kwargs['url']
            resp = requests.get(url)
            if resp.status_code == 200:
                with open(uaFile, 'rb') as fr, open(DB, 'wb') as fw:
                    fw.write(resp.content)
        elif uaDic.get(version):
            uaData = uaDic[version]
            with open(DB, 'w', encoding='utf-8') as fw:
                fw.write(json.dumps(uaData, ensure_ascii=False, indent=4))




def getWhiteList(whiteIpListUrl):
    if whiteIpListUrl:
        try:
            res = requests.get(whiteIpListUrl).json()
            lists = res['data']['lists']
            return list([item.get('mark_ip') for item in lists])
        except:
            pass
    return []

def initWhite(ip=None, whiteIpListUrl=None, whiteIpSaveUrl=None):
    origin = ip or getOrigin()
    whiteList = getWhiteList(whiteIpListUrl)
    if origin not in whiteList and whiteIpSaveUrl:
        while True:
            url = whiteIpSaveUrl + origin
            res = requests.get(url).json()
            print(res)
            msg = res.get('msg')
            if '再次请求' not in msg:
                break
            time.sleep(3)

def unzip(zipFilePath, output, kw='chromedriver'):
    b = zipfile.is_zipfile(zipFilePath)
    targetPath = zipFilePath
    if b:
        fz = zipfile.ZipFile(zipFilePath, 'r')
        for file in fz.namelist():
            if kw in fz.getinfo(file).filename:
                targetPath = fz.extract(file, output)

    return targetPath


def getDunTextReviewLabels(fileName='../File/dun_text_review_labels.txt'):
    dun_text_review_labels = {}
    with open(fileName, 'r', encoding='utf-8') as fr:
        data = fr.read()
        for line in data.split('\n'):
            if line.strip():
                label, subLabel, desc = line.split('\t')
                dun_text_review_labels.setdefault(label, {})
                dun_text_review_labels[label][subLabel] = desc

    return dun_text_review_labels

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8', 'ignore')
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        else:
            return False


def get_valueFmt(keys, digital=0):
    temp = []
    # :1,: 2,:3,: 4,:5,: 6,:7,: 8,:9,: 10,:11,: 12
    for i in range(len(keys)):
        if digital:
            temp.append(':' + str(i + 1))
        else:
            temp.append(':' + str(keys[i]))
    return ','.join(temp)


def parseYml(ymlFile):
    with open(ymlFile, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise yaml.YAMLError(exc)


def initConf(configFile):
    if isinstance(configFile, str) and os.path.exists(configFile):
        if configFile.endswith('ini'):
            return Settings(configFile)
        elif configFile.endswith('yaml') or configFile.endswith('yml'):
            return parseYml(configFile)
    else:
        raise ValueError(f"{configFile}: not File")


