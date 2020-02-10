import sqlite3
import time
import os
from threading import Thread
from config import config
import requests
class DB(object):
    def __init__(self,path=config["db"]["file"]):
        self.initalize(path)
    def initalize(self,path):
        table=False
        if config["db"]["refresh"]:
            os.remove(config["db"]["file"])
        if not os.path.exists(config["db"]["file"]):
            table=True
        self.db=sqlite3.connect(path,check_same_thread = False)
        self.cu=self.db.cursor()
        if table:
            self.cu.execute('''CREATE TABLE PROXY
            (IP TEXT NOT NULL,
            UPTIME TEXT NOT NULL,
            CONTURY TEXT NOT NULL);''')
            self.db.commit()
    def add(self,proxy):
        Thread(target=self.__add,args=(proxy,)).start()
    def __add(self,proxy,*arg):
        t=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        if isinstance(proxy,str):
            if config["db"]["update"]:
                if proxy not in self.getall():
                    self.cu.execute('''INSERT INTO PROXY (IP,UPTIME,CONTURY) \
                  VALUES (?,?,?);''',(proxy,t,self.getcontury(proxy)))
                else:
                    self.cu.execute('''UPDATE PROXY SET UPTIME=? WHERE IP=?;''',(t,proxy))
            else:
                self.cu.execute('''INSERT INTO PROXY (IP,UPTIME,CONTURY) \
              VALUES (?,?,?);''',(proxy,t,self.getcontury(proxy)))
            self.db.commit()
        else:
            for x in proxy:
                if config["db"]["update"]:
                    if proxy not in self.getall():
                        self.cu.execute('''INSERT INTO PROXY (IP,UPTIME,CONTURY) \
                    VALUES (?,?,?);''',(x,t,self.getcontury(x)))
                    else:
                        self.cu.execute('''UPDATE PROXY SET UPTIME=? WHERE IP=?;''',(t,x))
                else:
                    self.cu.execute('''INSERT INTO PROXY (IP,UPTIME,CONTURY) \
                VALUES (?,?,?);''',(x,t,self.getcontury(x)))
            self.db.commit()
    def remove(self,proxy):
        self.cu.execute("DELETE from PROXY where IP=?;",(proxy))
        self.db.commit()
    def getall(self):
        cursor = [x[0] for x in list(filter(None,list(self.cu.execute("SELECT IP,UPTIME,CONTURY from PROXY"))))]
        self.db.commit()
        return cursor
    def get(self):
        cursor = list(filter(None,list(self.cu.execute("SELECT IP,UPTIME,CONTURY from PROXY"))))
        self.db.commit()
        return cursor
    def gettime(self,proxy):
        cursor = [x[1] for x in list(filter(None,list(self.cu.execute("SELECT IP,UPTIME,CONTURY from PROXY")))) if x[0]==proxy]
        self.db.commit()
        return cursor
    def getcontury(self,proxy):
        r=requests.get("http://whois.pconline.com.cn/ipJson.jsp?ip=%s&json=true"%proxy)
        if r.json()["err"]!="":
            return "未知"
        return r.json()["addr"].split(" ")[0]
    def getdbcontury(self,proxy):
        cursor = [x[2] for x in self.getall() if x[0]==proxy]
        self.db.commit()
        return cursor
    def __del__(self):
        self.db.close()
