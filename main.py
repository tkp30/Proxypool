from printer import *
from threading import Thread
from webapi import run
from crawl import Crawler
from tests import Tester
from config import config
import time
class Scheduler():
    def test(self, cycle, url, *a):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            info('[调度系统] 测试器开始运行')
            info("[调度系统] 测试使用的URL："+config["test"]["url"])
            tester.run()
            time.sleep(int(cycle))
    
    def get(self, cycle, *a):
        """
        定时获取代理
        """
        getter = Crawler()
        while True:
            info('[调度系统] 开始抓取代理')
            getter.run()
            if config["crawl"]["checkmax"]:
                if len(DB().getall())>=config["crawl"]["maxvalue"]:
                    info("[调度系统] 代理池已达上限，停止抓取代理")
                    while len(DB().getall())>=config["crawl"]["maxvalue"]:pass
            time.sleep(int(cycle))
    
    def api(self,*a):
        """
        开启API
        """
        run()
    
    def run(self):
        warning('[调度系统] 代理池开始运行')
        t1=Thread(target=self.get,args=(str(config["crawler"]["cycle"])))
        t2=Thread(target=self.test,args=(str(config["test"]["cycle"]),config["test"]["url"]))
        t3=Thread(target=self.api)
        if config["test"]["open"]:
            t2.start()
        if config["crawler"]["open"]:
            t1.start()
        if config["web"]["open"]:
            t3.start()
s=Scheduler()
s.run()
