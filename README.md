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
* 89IP(http://89ip.cn/)
* 西刺代理（会封IP 503，建议不要使用。停用方法：打开crawl.py把crawl_xici换成ncrawl_xici，不好用的我都注释上了，http://xicidaili.com/）
* ip.yqie.com（我也不知道这个网站叫什么）
* 西拉代理（http://xiladaili.com/)
* 泥马代理（http://nimadaili.com/)
* 旗云代理（http://7yip.com/）
* wndaili.com（我也不知道这个网站叫什么）
* 三一代理（http://31f.cn）
* 云代理（http://www.ip3366.net/)
* www.thebigproxylist.com（无名网站）
* 飞蚁代理（很隐蔽，直接贴代理列表吧：http://www.feiyiproxy.com/?page_id=1457)
* LASSIN的编程实验室（https://lab.crossincode.com/）
* http://ip.syssuper.com:8000/ip.php（无名网站）
* ~~快代理~~~（容易封IP，https://www.kuaidaili.com/）
* ~~http://www.superfastip.com/~~（我也不知道这个网站叫什么，容易封IP）
