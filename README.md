## Sqlmapapi批量化扫描支持GET+POST+COOKIE类型扫描

#### 使用方法

~~~
启动sqlmapapi服务：
	python sqlmapapi.py -s
构建测试住点的txt文件
	例：
		http://dfsfsd.coms/home/?id=1              #GET型注点
		http://地址*username=1                     #POST类型注点
		http://地址*cookie:name=1                  #注点参数在cookie 
         http://地址*referer:name=1                 #注点参数在referer 
     一行一个测试点，有参数格式是住点 地址*参数名
     cookie和referer的格式是：地址*cookie/referer:参数名
     
     时间关系型没做参数化的处理
	 代码clone 
	 修改 144行 server参数  填写你运行sqlmapapi的地址
	 直接使用pycharm运行
	 
运行环境
	版本 python3 
	库 requests
~~~

## file_scan、SubDom_Query

~~~
file_scan      简单的基于字典的多线程扫描脚本
SubDom_Query   简单的基于字典的子域名扫描脚本
~~~

