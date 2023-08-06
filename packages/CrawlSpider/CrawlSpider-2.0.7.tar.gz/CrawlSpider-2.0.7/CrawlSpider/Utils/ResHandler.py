from typing import Tuple

from CrawlSpider.Utils.FileUpload import FileUpload, urlparse, List
from bs4 import BeautifulSoup,Tag
import asyncio


class ImgSrcReplace:
    @classmethod
    async def wxgzh(cls, body:str='', soup:Tag=None, fileUpload: FileUpload = None)->Tag:
        """
        body和soup两者必须有一个有值
        :param body: tag的字符串形式
        :param soup: Tag类型的节点
        :param fileUpload: FileUpload 用于将文件资源上传到云存储
        :return: 返回节点字符串形式
        """
        soup = soup or BeautifulSoup(body, 'lxml')

        imgs: List[Tag] = soup.find_all(name='img')
        for img in imgs:
            data_src = img.get('data-src')
            # 判空操作
            if not data_src:
                continue
            data = await fileUpload.uploadFileFromNetToOss(data_src)
            url = data.get('url')
            if url:
                img.attrs.pop('data-src')
                img.attrs.update({
                    'src': url
                })
        return soup

    @classmethod
    async def common(cls, body: str = '', imgAttrName:str='src', sleep=0.05, imgFilePattern=None, imgFileScope:str=None, fileUpload: FileUpload = None) -> \
    Tuple[str, str]:
        """
        body和soup两者必须有一个有值
        :param body: tag的字符串形式
        :param fileUpload: FileUpload 用于将文件资源上传到云存储
        :return: 返回节点字符串形式
        """
        soup = BeautifulSoup(body, 'lxml')
        soup = await LinkHrefReplace.common(soup=soup)
        imgs: List[Tag] = soup.find_all(name='img')
        for img in imgs:
            data_src:str = img.get(imgAttrName)
            if not data_src:
                continue
            imgUrl = data_src
            res = urlparse(data_src)

            if '192.168' not in res.netloc:
                if not res.netloc and not imgFileScope:
                    return body, "图片地址非绝对路径，请传imgFileScope前缀"
                if data_src.startswith('/'):
                    result = urlparse(imgFileScope)
                    imgUrl = f"{result.scheme}://{result.netloc}{data_src}"
                else:
                    # suffix = listUrl.split('/')[-1]
                    # prefix = listUrl.rstrip(suffix)
                    # realUrl = prefix + detailUrl
                    # url.rstrip(url.split('/')[-1])
                    if data_src.startswith('.'):
                        imgUrl = imgFileScope + data_src
                    if not res.scheme and data_src.startswith("//"):
                        scheme = urlparse(imgFileScope).scheme
                        imgUrl = f'{scheme}:{data_src}'
                data = await fileUpload.uploadFileFromNetToOssCommon(imgUrl)
            else:
                data = {
                    'url': None
                }
            realUrl = data.get('url') or ''
            img.attrs.update({
                'src': realUrl,
                'data-src': '',
                'oldsrc': ''
            })
            await asyncio.sleep(delay=sleep)
        return soup.decode(),"图片和链接置换成功"

    @classmethod
    async def delTagsExceptImg(cls, htmlStr: str = None, soup=None, imgAttr='src'):
        soup = soup or BeautifulSoup(htmlStr or "", 'lxml')
        imgs = soup.find_all(name='img')
        for img in imgs:
            img: Tag
            data_src = img.get(imgAttr)
            if not data_src:
                continue
            s = f'###p***###img src="{data_src}"***###/p***'
            img.append(s)
        # 文本都包在p标签中
        res = soup.get_text(separator="<p>", strip=True)
        res = res.strip('<p>')
        # 实现首行缩进 style="text-indent:2em"
        res = res.replace('<p>', '</p><p>')
        res = res.replace('###', '<')
        res = res.replace('***', '>')
        # return f"<p>{res}</p>"
        return res

class LinkHrefReplace:
    @classmethod
    async def common(cls, body:str='', soup:Tag=None)->Tag:
        """
        body和soup两者必须有一个有值
        :param body: tag的字符串形式
        :param soup: Tag类型的节点
        :return: 返回节点字符串形式
        """
        soup = soup or BeautifulSoup(body, 'lxml')
        aLinks: List[Tag] = soup.find_all(name='a')
        for link in aLinks:
            href = link.get('href')
            if href:
                link['href'] = ''
        return soup


class VideoSrcReplace:
    @classmethod
    async def wxgzh(cls, body:str='', soup:Tag=None, fileUpload: FileUpload = None)->str:
        """
        body和soup两者必须有一个有值
        :param body: tag的字符串形式
        :param soup: Tag类型的节点
        :param fileUpload: FileUpload 用于将文件资源上传到云存储
        :return: 返回节点字符串形式
        """
        soup = soup or BeautifulSoup(body, 'lxml')

        imgs: List[Tag] = soup.find_all(name='img')
        for img in imgs:
            data_src = img.get('data-src')
            data = await fileUpload.uploadFileFromNetToOss(data_src)
            url = data.get('url')
            if url:
                img.attrs.pop('data-src')
                img.attrs.update({
                    'src': url
                })
        return soup.decode()