import sqlite3
import time
import os
from config import config
import requests
class DB(object):
    def __init__(self,path=config["db"]["file"]):
        self.initalize(path)
    def initalize(self,path):
        '''初始化函数'''
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
            CONTURY TEXT NOT NULL,
            OPERATORS TEXT NOT NULL);''')
            self.db.commit()
    def add(self,proxy):
        '''非阻塞加入代理'''
        for x in proxy:
            self.__add(x)
    def __add(self,proxy,*arg):
        '''加入代理底层接口'''
        t=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        c=self.getcontury(proxy)
        if not config["db"]["update"]:
            if proxy not in self.getall():
                self.db.execute('''INSERT INTO PROXY (IP,UPTIME,CONTURY,OPERATORS) \
            VALUES (?,?,?,?);''',(proxy,t,c[0],c[1]))
            else:
                self.db.execute('''UPDATE PROXY SET UPTIME=? WHERE IP=?;''',(t,proxy))
        else:
            self.db.execute('''INSERT INTO PROXY (IP,UPTIME,CONTURY,OPERATORS) \
        VALUES (?,?,?,?);''',(proxy,t,c[0],c[1]))
        try:
            self.db.commit()
        except:
            pass
    def remove(self,proxy):
        '''删除代理'''
        self.cu.execute("DELETE from PROXY where IP=?;",(proxy))
        self.db.commit()
    def getall(self):
        '''获取全部代理'''
        cursor = [x[0] for x in list(filter(None,list(self.cu.execute("SELECT IP,UPTIME,CONTURY,OPERATORS from PROXY"))))]
        self.db.commit()
        return cursor
    def get(self):
        '''获取全部代理及数据'''
        cursor = list(filter(None,list(self.cu.execute("SELECT IP,UPTIME,CONTURY,OPERATORS from PROXY"))))
        self.db.commit()
        return cursor
    def gettime(self,proxy):
        '''获取某个代理的更新时间'''
        cursor = [x[1] for x in list(filter(None,list(self.cu.execute("SELECT IP,UPTIME,CONTURY,OPERATORS from PROXY")))) if x[0]==proxy]
        self.db.commit()
        return cursor
    def getcontury(self,proxy):
        '''IP定位'''
        r=requests.get("http://whois.pconline.com.cn/ipJson.jsp?ip=%s&json=true"%proxy)
        if r.json()["err"]!="":
            return ["未知"]*2
        return r.json()["addr"].split(" ")
    def getdbcontury(self,proxy):
        '''获取已有IP的地区'''
        cursor = [x[2] for x in self.get() if x[0]==proxy]
        self.db.commit()
        return cursor
    def __del__(self):
        '''销毁方法'''
        self.db.close()
