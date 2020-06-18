from pymongo import MongoClient
import requests
import time
class DB(object):
    def __init__(self,path=config["db"]["file"]):
        self.initalize(path)
    def initalize(self,path):
        client=pymongo.MongoClient(path)
        if config["db"]["refresh"] and "proxypool" in client.list_database_names():
            client.dropDatabase(client.proxypool)
        self.db=client["proxypool"]["proxy"]
    def add(self,proxy):
        for x in proxy:
            self.__add(x)
    def __add(self,proxy,*arg):
        t=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        c=self.getcontury(proxy)
        self.db.insert({
            "IP":proxy,
            "UPTIME":t,
            "CONTURY":c[0],
            "OPERATORS":c[1]
        })
    def remove(self,proxy):
        self.db.remove({"IP":proxy})
    def getall(self):
        return [x["IP"] for x in self.get()]
    def get(self):
        return list(self.db.find())
    def gettime(self,proxy):
        return self.db.find({"IP":proxy})[0]["UPTIME"]
    def getdbcontury(self,proxy):
        return self.db.find({"IP":proxy})[0]["CONTURY"]
    def getinfo(self,proxy):
        s=self.db.find({"IP":proxy})[0]
        return {
            "ip":proxy,
            "uptime":s["UPTIME"],
            "contury":s["CONTURY"],
            "operators":s["OPERATORS"]
        }
    def getcontury(self,proxy):
        r=requests.get("http://whois.pconline.com.cn/ipJson.jsp?ip=%s&json=true"%proxy)
        if r.json()["err"]!="":
            return ["未知"]*2
        return [r.json()["addr"].split(" ")[0],r.json()["addr"].split(" ")[1].strip("ADSL")]
        
