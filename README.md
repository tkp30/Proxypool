# Proxypool
### Python免费代理池。
> 走过路过给个star......

依赖包：
* Flask
* requests
* bs4
* dict4ini（**不要用pip，PYPI没有，请在Github上找**）

适用于Python 3.5以上版本。
部分逻辑参照 [*崔庆才老师*](http://cuiqingcai.com/) 的书《Python网络爬虫开发实战》。
建议不要`git clone https://github.com/XHG78999/Proxypool.git`，我放了个一万八行的UA列表会卡炸（反反爬用）

目前爬取网站有：
* 89IP (http://89ip.cn/)
* 西刺代理（会封IP 503，建议不要使用。停用方法：打开crawl.py把crawl_xici换成ncrawl_xici，不好用的我都注释上了，http://xicidaili.com/ ）
* http://ip.yqie.com (我也不知道这个网站叫什么）
* 西拉代理(http://xiladaili.com/)
* 泥马代理(http://nimadaili.com/)
* 旗云代理(http://7yip.com/)
* http://wndaili.com (我也不知道这个网站叫什么)
* 三一代理(http://31f.cn)
* 云代理(http://www.ip3366.net/)
* www.thebigproxylist.com （无名网站)
* 飞蚁代理(很隐蔽，直接贴代理列表吧：http://www.feiyiproxy.com/?page_id=1457 )
* LASSIN的编程实验室(https://lab.crossincode.com/)
* http://ip.syssuper.com:8000/ip.php (无名网站)
* ~~快代理~~(容易封IP，https://www.kuaidaili.com/)
* ~~http://www.superfastip.com/~~(我也不知道这个网站叫什么，容易封IP)

结构：
crawl.py -> 代理爬虫
database.py -> SQLite数据库API
tests.py -> 代理测试器
printer.py -> **Windows**下的彩色日志输出。
ua1.txt -> UserAgent列表
config.ini -> 配置文件
config.py -> 配置处理文件

config.ini说明：
`
[test]
url=http://httpbin.org/get #测试用的URL
method=future              #测试用方法，future或no（单线程）
threads=40                 #测试线程数
cycle=20                   #循环等待时间
timeout=5                  #超时时间
completion=1               #自动补足开关，仅在爬取器关闭时可用
completion_thowsold=5000   #自动补足阈值
open=1                     #开关
[crawler]                  
checkmax=1                 #池子大小限制开关        
maxvalue=60000             #最大限制
cycle=30                   #执行间隔
open=1                     #开关
[db]
file=proxies.sqlite        #数据库文件
refresh=0                  #是否刷新（在重启时）
update=1                   #替换开关
[web]
ip=127.0.0.1               #REST API运行IP
port=80                    #REST API运行端口
open=1                     #开关
`

有问题开ISSUE并加个Pullrequest。

运行：
`python3 main.py`
谢谢！！
