from printer import info,ok,error,warning
from database import DB
from config import config
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import Pool
from threading import Thread
from crawl import Crawler
import time
import requests
import time
class Tester(object):
    db=DB()
    thowsold=config["test"]["completion_thowsold"]
    parse=False
    errors=0
    def test_one(self,pro):
        proxy={
        "http":"http://"+pro,
        "https":"https://"+pro
        }
        m=10
        while m>0:
            try:
                t=time.time()
                r=requests.get(config["test"]["url"],timeout=config["test"]["timeout"])
                assert r.ok,"状态码错误"
                info("[测试器] 代理可用"+pro.ljust(21)+" 请求用时"+str(round(time.time()-t,2))+"s")
                return
            except Exception as e:
                error("[测试器] 代理超时"+pro.ljust(22)+"准备重试")
                errors+=1
                continue
        error("[测试器] 代理无法使用"+pro+"移除")
        self.db.remove(pro)
    def completion(self,*args):
        info("[测试器] 启动自动补足程序")
        self.parse=True
        self.errors=0
        Crawler.run()
        self.parse=False
    def run(self):
        info("[测试器] 开始运行测试器")
        if config["test"]["method"]=="no":
            for x in self.db.getall():
                self.test_one(x)
            if self.errors>=self.thowsold and not self.parse:
                if config["crawl"]["open"]:
                    error("[测试器] 爬取器已经运行，无法启动自动补足程序")
                else:
                    t=threading.Thread(target=self.completion)
                    t.start()
        elif config["test"]["method"]=="future":
            with ThreadPoolExecutor(config["test"]["threads"]) as e:
                e.map(self.test_one,self.db.getall())
            if self.errors>=self.thowsold and not self.parse:
                if config["crawl"]["open"]:
                    error("[测试器] 爬取器已经运行，无法启动自动补足程序")
                else:
                    t=threading.Thread(target=self.completion)
                    t.start()
