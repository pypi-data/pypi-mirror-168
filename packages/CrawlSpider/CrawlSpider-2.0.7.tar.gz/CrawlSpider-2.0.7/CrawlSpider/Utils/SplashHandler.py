
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from CrawlSpider.Utils.FileUtils import mkdir
from CrawlSpider.Utils.Helper import downloadFileFromInet
from CrawlSpider.conf.settings import chromePath, chromeDriverDwnUrl
import time
import copy
import os
import platform
sysType = platform.system()


class WebSplash:
    def __init__(self, chromedriverPath=None, **kwargs):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')

        
        # close chrome
        # chrome_options.add_experimental_option("detach", True)
        ## 不显示"chrome正受到自动测试软件的控制"
        # chrome_options.add_argument('disable-infobars')

        self.chrome_options = chrome_options
        # 无头浏览器需要传入参数在实例化的浏览器对象中*****
        self.driver: webdriver.Chrome = None
        # 让浏览器指定url发起请求 经测试它有动态加载数据
        self.chromedriverPath = chromedriverPath
        self.initDriver(chromedriverPath=chromedriverPath, **kwargs)

    def initDriver(self, chromedriverPath=None, version=None, **kwargs):
        # '//chromedriver_win32.zip'

        if not chromedriverPath:
            version = version or '102.0.5005.61'
            chromeDriverName = 'chromedriver_win32' if sysType == 'Windows' else 'chromedriver_linux64' if sysType == 'Linux' else 'chromedriver_mac64'
            chromeDriverDir = mkdir(f".chrome_driver/{version}")
            pathList = os.listdir(chromeDriverDir)
            if len(pathList) != 1 or pathList[0].endswith('zip'):
                chromedriverPath = downloadFileFromInet(f"{chromeDriverDwnUrl}/{version}/{chromeDriverName}.zip", outputDir=chromeDriverDir, outFile=f"{chromeDriverName}.zip")
                # 给 Linux 上的文件赋予可执行权限
                if sysType == 'Linux' and os.path.exists(chromedriverPath):
                    os.system(f"chmod 777 {chromedriverPath}")
            else:
                chromedriverPath = os.path.join(chromeDriverDir, pathList[0])

        self.chromedriverPath = chromedriverPath

    def getSource(self, url, driver=None, splashTime=0.2):
        # 无头浏览器设置（*********增加爬取效率）
        if not driver:
            driver = self.getNewDriver()

        driver.get(url)
        # sleep 0.2s
        time.sleep(splashTime)
        page_source: str = driver.page_source
        # 关闭当前标签页,一直使用get请求，其实使用的都是main标签页，所以不要在这里关闭，一旦关闭就表示浏览器也被关闭
        # driver.close()
        return {
            'content': page_source.encode(),
            'driver': driver
        }

    def disconnect(self):
        if sysType == 'Windows':
            try:
                import win32process
                print(u"正在关闭Chrome进程")
                self.driver.close()
                self.driver.quit()
                win32process.TerminateProcess(self.chrome[0], 0)
                os.system("taskkill /IM software_reporter_tool.exe /F")
            except Exception as e:
                print(f"e:{e}")


    def getDriver(self, options: list=None):
        if not options:
            if hasattr(self, 'driver') and self.driver:
                return self.driver
            else:
                self.driver = webdriver.Chrome(executable_path=self.chromedriverPath, options=self.chrome_options)
                return self.driver
        else:
            chrome_options = copy.deepcopy(self.chrome_options)
            chrome_options.arguments.extend(options)
            driver = webdriver.Chrome(executable_path=self.chromedriverPath, options=chrome_options)
            return driver


    def getNewDriver(self, options:list=None, isHeadless=True, debugger_address=None):



        chrome_options = copy.deepcopy(self.chrome_options)
        if options:
            chrome_options.arguments.extend(options)
        if '--headless' not in chrome_options.arguments or not isHeadless:
            chrome_options.headless = isHeadless

        if debugger_address:
            chrome_options.debugger_address = debugger_address

        self.driver = webdriver.Chrome(executable_path=self.chromedriverPath, options=chrome_options)
        return self.driver

    def launch_chrome(self, chrome_debugger_port=9224):
        if sysType == 'Windows':
            import win32process
            self.chrome_port = chrome_debugger_port
            if os.path.exists(chromePath):
                command = f"'{chromePath}' --remote-debugging-port={chrome_debugger_port}"
                print(u"如果Chrome白屏，请使用CMD手动运行以下命令:\n{}".format(command))
                self.chrome = win32process.CreateProcess(None, "{} --remote-debugging-port={}".format(chromePath,
                                                                                                      self.chrome_port),
                                                         None, None, 0, 0, None, None, win32process.STARTUPINFO())
            else:
                print(u"未找到Chrome安装目录")
                exit(-1)
            return f"127.0.0.1:{self.chrome_port}"

    def connect(self, options:list=None, page_load_timeout=60, script_timeout=60, chrome_debugger_port=9224, isHeadless=True):
        debugger_address = self.launch_chrome(chrome_debugger_port=chrome_debugger_port)
        driver = self.getNewDriver(options=options, isHeadless=isHeadless, debugger_address=debugger_address)
        driver.set_page_load_timeout(page_load_timeout)
        driver.set_script_timeout(script_timeout)
        return driver

webSplash = WebSplash()


