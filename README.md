```
              ______    ______
             |_    _|  | ____ \     
               |  |    | |__| |   
               |  |    | _____/
             __|  |__  | |
             |______|  |_|

                 免费代理池
              Free Proxy Pool
```
# Proxypool
### Python免费代理池。
> 走过路过给个star......

***
⚠    声明：
受限于环境问题，作者无法将所有主流数据库全部写上驱动。如有热心网友手头有环境的，请帮忙按照database.py的格式写一份数据库驱动。
如果写好了，请联系572747232@qq.com，将代码以附件形式发送，来信请注明Proxypool Database。

编写不易，如果需要fork，请***至少做出一些更改！！！***
***

依赖包：
* Flask
* requests
* bs4
* dict4ini（https://github.com/ZoomQuiet/dict4ini）

适用于Python 3.2以上版本。(因为用到了`yield from`）
部分逻辑参照 [*崔庆才老师*](http://cuiqingcai.com/) 的书《Python网络爬虫开发实战》。
建议不要`git clone https://github.com/XHG78999/Proxypool.git`，我放了个一万八行的UA列表会卡炸（反反爬用）

目前爬取网站有：
* 89IP (http://89ip.cn/)
* 西刺代理（http://xicidaili.com/ ）
* YQIE代理 (http://ip.yqie.com） 
* 西拉代理(http://xiladaili.com/)
* 泥马代理(http://nimadaili.com/)
* 旗云代理(http://7yip.com/)
* http://wndaili.cn (我也不知道这个网站叫什么)
* 三一代理(http://31f.cn)
* 云代理(http://www.ip3366.net/) ℹ  网站增强反扒措施，即将移除
* www.thebigproxylist.com （无名网站)
* ~~飞蚁代理(很隐蔽，直接贴代理列表吧：http://www.feiyiproxy.com/?page_id=1457 ) 网站改版已失效 ~~
* LASSIN的编程实验室(https://lab.crossincode.com/)
* 快代理(https://www.kuaidaili.com/)
* 极速代理(http://www.superfastip.com/)
* 66IP(http://66ip.cn)
* 开心代理(http://kxdaili.com)
* 高可用全球代理IP库(https://ip.jiangxianli.com/)

结构：<br />
crawl.py -> 代理爬虫<br />
database.py -> SQLite数据库API<br />
tests.py -> 代理测试器<br />
printer.py -> **Windows**下的彩色日志输出。如果是用苹果和Linux的技术宅请自行更换<br />
ua1.txt -> UserAgent列表<br />
config.ini -> 配置文件<br />
config.py -> 配置处理文件<br />

config.ini说明：
```
[test]
url=http://httpbin.org/get #测试器URL
method=future                #测试方法
threads=10                     #测试线程数
cycle=120                      #间隔时间
timeout=5                      #超时时间
completion=1                 #自动补足
completion_thowsold=5000 #自动补足阈值
open=1                          #开关
output=0                       #静默模式
[crawler]
checkmax=1                  #检测上限 
maxvalue=100000          #上限值
cycle=30                       #间隔时间
open=1                         #开关
output=1                      #静默模式
[db]
file=proxies.sqlite          #数据库路径
refresh=0                     #每次启动是否刷新
update=1                     #是否去重
[web]
ip=127.0.0.1                 #Web API地址
port=80                       #Web API端口
open=1                       #开关
```

运行方式：
```
pip install -r requirements.txt
```

更新记录：<br />
***2020-2-10***<br />
    创建存储库。<br />
***2020-2-11***<br />
    更新了数据库驱动，让数据库可正常处理。<br />
***2020-2-12***<br />
    更新了WebAPI和爬取器，重新启用了被弃用的两个网站。<br />
***2020-2-15***<br />
    更新了爬取器，弃用一个网站，启用一个网站。<br />
***2020-3-13***<br />
    更新爬取器和调度器，重新启动三一代理，删除了一些多余的东西，并改用多进程。
    增加requirements.txt<br />
***2020-4-19***<br />
    预告：将增加对MongoDB的支持。如果您想兼容其他数据库，可以分叉这个存储库，在分叉中做修改，我会考虑加入到主存储库里。<br />
***2020-6-18***<br />
    MongoDB支持已添加，位于Mongo分支中。需要使用MongoDB驱动的网友们可以将config.ini,database.py替换为Mongo分支中的config.ini和database.py。<br />
***2020-6-20***<br />
    应网站改版，停用或修改部分爬虫，结构回退（因爬取器多线程跑太快有一定概率烧网卡【滑稽】）<br />
