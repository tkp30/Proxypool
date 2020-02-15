import requests
import chardet
from bs4 import BeautifulSoup
from database import DB
import re
import socket
import random
import time
from printer import *
def get_agent():
    return random.choice(open("ua1.txt",encoding="utf-8").read().split("\n"))
def get_page(url):
    try:
        while True:
            r=requests.get(url,headers={"User-Agent": get_agent()})
            #assert r.status==200
            if r.status_code==503:
                error("503拒绝服务")
                return None
            assert r.ok,"状态码错误"
            r.encoding=chardet.detect(bytes(r.content))["encoding"]
            #return r.text.strip("\t").strip("\n")
            return r.text.strip().strip("\n")
    except Exception as e:
        error("爬虫发生错误"+str(e))
        #error(r.text)
        return None
    
class ProxyMetaclass(type):
    def __new__(cls,names,bases,attrs):
        count=0
        attrs["__CrawlFunc__"]=[]
        for k,v in attrs.items():
            if k.startswith("crawl_"):
                attrs["__CrawlFunc__"].append(k)
                attrs["__CrawlFunc__"].sort()
                count+=1
        attrs["__CrawlFuncCount__"]=count
        return type.__new__(cls,names,bases,attrs)
class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies=[]
        try:
            for proxy in eval("self.{}()".format(callback)):
                ok("[获取器] 成功获取代理%s"%proxy)
                proxies.append(proxy)
            warning("[获取器] 共获取IP %s个"%len(proxies))
            return proxies
        except Exception as e:
            error(str(e))
            return []
    def crawl_89ip(self):
        url="http://www.89ip.cn/tqdl.html?api=1&num=1000&port=&address=&isp="
        printSkyBlue("[获取器] 正在爬取"+url)
        page=get_page(url)
        if page:
            yield from re.findall(r"\d+\.\d+\.\d+\.\d+\:\d+",page)
    def ncrawl_89ip(self): #已失效
        url="http://www.89ip.cn/index_{}.html"
        urls=[url.format(page) for page in range(1,7)]
        for url in urls:
            printSkyBlue("[获取器] 正在爬取"+url)
            page=get_page(url)
            if page:
                ip=[x.strip("<td>").strip("</td>") for x in re.findall("\d+\.\d+\.\d+\.\d+",page,re.S)]
                port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page,re.S)]
                for x in zip(ip,port):
                    yield ":".join(x)
    def crawl_xici(self):
        urls2=["https://www.xicidaili.com/nn/{}","https://www.xicidaili.com/nt/{}","https://www.xicidaili.com/nt/{}","https://www.xicidaili.com/wt/{}","https://www.xicidaili.com/qq/{}"]
        for urI in urls2:
            urls=[urI.format(x) for x in range(1,201)]
            for url in urls:
                printSkyBlue("[获取器] 正在爬取"+url)
                page=get_page(url)
                ip=re.findall("\d+\.\d+\.\d+\.\d+",page)
                port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page)]
                for x in zip(ip,port):
                    yield ":".join(x)
                time.sleep(2)
    def crawl_kuaidaili(self):
        urls2=["https://www.kuaidaili.com/free/inha/{}/","https://www.kuaidaili.com/free/intr/{}/"]
        for url in urls2:
            urls=[url.format(page) for page in range(1,50)]
            for url in urls:
                printSkyBlue("[获取器] 正在爬取"+url)
                page=get_page(url)
                if page:
                    bs=BeautifulSoup(page,"html.parser")
                    ip=[str(x).strip('<td data-title="IP">').strip("</td>") for x in bs.find_all("td",attrs={"data-title":"IP"})]
                    port=[str(x).strip('<td data-title="PORT">').strip("</td>") for x in bs.find_all("td",attrs={"data-title":"PORT"})]
                    for x in zip(ip,port):
                        yield ":".join(x)
                time.sleep(3)

    def crawl_yqie(self):
        url="http://ip.yqie.com/ipproxy.htm"
        printSkyBlue("[获取器] 正在爬取"+url)
        page=get_page(url)
        if page:
            ip=re.findall("\d+\.\d+\.\d+\.\d+",page)
            port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page)]
            for x in zip(ip,port):
                yield ":".join(x)
    def crawl_xila(self):
        url="http://www.xiladaili.com/putong/{}/"
        urls=[url.format(page) for page in range(1,51)]
        for url in urls:
            printSkyBlue("[获取器] 正在爬取"+url)
            page=get_page(url)
            if page:
                ip=re.findall("\d+\.\d+\.\d+\.\d+:\d+",page)
                yield from ip
            time.sleep(3)
    def crawl_nima(self):
        urls2=["http://www.nimadaili.com/gaoni/{}","http://www.nimadaili.com/http/{}","http://www.nimadaili.com/https/{}"]
        for urI in urls2:
            urls=[urI.format(x) for x in range(1,51)]
            for url in urls:
                printSkyBlue("[获取器] 正在爬取"+url)
                page=get_page(url)
                if page:
                    yield from re.findall("\d+\.\d+\.\d+\.\d+\:\d+",page)
                time.sleep(2)
            
    def crawl_7yun(self):
        url="https://www.7yip.cn/free/?action=china&page={}"
        urls=[url.format(page) for page in range(1,51)]
        for url in urls:
            printSkyBlue("[获取器] 正在爬取"+url)
            page=get_page(url)
            if page:
                bs=BeautifulSoup(page,"html.parser")
                ip=[str(x).strip('<td data-title="IP" class="has-responsive-th"><span class="responsive-th">IP</span>').strip("</td>") for x in bs.find_all("td",attrs={"data-title":"IP"})]
                port=[str(x).strip('<td data-title="IP" class="has-responsive-th"><span class="responsive-th">PORT</span>').strip("</td>") for x in bs.find_all("td",attrs={"data-title":"PORT"})]
                for x in zip(ip,port):
                    yield ":".join(x)
    def crawl_wndaili(self):
        url="http://www.wndaili.cn/free/?stype=2&page={}"
        urls=[url.format(x) for x in range(1,31)]
        for url in urls:
            printSkyBlue("[获取器] 正在爬取"+url)
            page=get_page(url)
            if page:
                ip=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+\.\d+\.\d+\.\d+</td>",page)]
                port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page)]
                for x in zip(ip,port):
                    yield ":".join(x)
    def crawl_spfs(self):
        url="http://www.superfastip.com/welcome/freeip/{}"
        urls=[url.format(x) for x in range(1,11)]
        for url in urls:
            printSkyBlue("[获取器] 正在爬取"+url)
            page=get_page(url)
            if page:
                ip=re.findall(r"\d+\.\d+\.\d+\.\d+")
                port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page)]
                for x in zip(ip,port):
                    yield ":".join(x)
            time.sleep(5)
    def ncrawl_31f(self): #网站关闭
        urls=["http://31f.cn/https-proxy/","http://31f.cn/http-proxy/"]
        for url in urls:
            printSkyBlue("[获取器] 正在爬取"+url)
            page=get_page(url)
            if page:
                ip=re.findall(r"\d+\.\d+\.\d+\.\d+",page)
                port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page)]
                for x in zip(ip,port):
                    yield ":".join(x)
    def crawl_3366(self):
        urls2=["http://www.ip3366.net/free/?stype=1&page={}","http://www.ip3366.net/free/?stype=2&page={}"]
        for urI in urls2:
            urls=[urI.format(x) for x in range(1,51)]
            for url in urls:
                printSkyBlue("[获取器] 正在爬取"+url)
                page=get_page(url)
                if page:
                    ip=re.findall("\d+\.\d+\.\d+\.\d+",page)
                    port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page)]
                    for x in zip(ip,port):
                        yield ":".join(x)
                time.sleep(5)
    def crawl_iplist(self):
        url="http://www.thebigproxylist.com/members/proxy-api.php?output=all&user=list&pass=8a544b2637e7a45d1536e34680e11adf"
        printSkyBlue("[获取器] 正在爬取"+url)
        page=get_page(url)
        if page:
            yield from [x.split(",")[0] for x in page.split("\n")]
    def crawl_proxyant(self):
        url="http://www.feiyiproxy.com/?page_id=1457"
        printSkyBlue("[获取器] 正在爬取"+url)
        page=get_page(url)
        if page:
            ip=re.findall("\d+\.\d+\.\d+\.\d+",page)
            port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page)]
            for x in zip(ip,port):
                yield ":".join(x)
    def crawl_lassin(self):
        url="https://lab.crossincode.com/proxy/"
        printSkyBlue("[获取器] 正在爬取"+url)
        page=get_page(url)
        if page:
            ip=re.findall("\d+\.\d+\.\d+\.\d+",page)
            port=[x.strip("<td>").strip("</td>") for x in re.findall("<td>\d+</td>",page)]
            for x in zip(ip,port):
                yield ":".join(x)
    def crawl_syssuper(self):
        url="http://ip.syssuper.com:8000/ip.php"
        printSkyBlue("[获取器] 正在爬取"+url)
        page=get_page(url)
        getip=lambda domain:socket.getaddrinfo(domain, 'http')[0][4][0]
        if page:
            ip=re.findall(r"\d+\.\d+\.\d+\.\d+",page)
            coms=re.findall(r"\w+\.yunip168\.com",page)
            ip+=[getip(x) for x in coms]
            yield from [x+":80" for x in ip]
    def crawl_daili66(self):
        url="http://www.66ip.cn/mo.php?sxb=&tqsl=1000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D1000%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio"
        printSkyBlue("[获取器] 正在爬取"+url)
        page=get_page(url)
        if page:
            yield from re.findall(r"\d+\.\d+\.\d+\.\d+\:\d+",page)
    def run(self):
        db=DB()
        warning("[获取器] 开始执行爬虫")
        for call in self.__CrawlFunc__:
            pr=self.get_proxies(call)
            db.add(list(pr))
