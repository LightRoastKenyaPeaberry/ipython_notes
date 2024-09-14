# python爬虫--B站python研究社

## chap1. 初识爬虫



### 最简单的例子

```python
from urllib.request import urlopen

url = 'http://www.baidu.com'
req = urlopen(url)

with open('mybaidu.html', 'w') as f: 
	f.write(req.read().decode('utf-8'))
  
print('over!')  

req.close() 
```



### web请求过程

每当我们向网页请求某些数据时： 

1. 服务器渲染： 在服务器那边直接把数据和html整合在一起，统一返回给浏览器(一次请求，一次返回)。在页面源代码中能看到数据。
2. 客户端渲染： 第一次请求，第一次返回html骨架；第二次请求，第二次返回数据。在页面源代码中看不到数据。
   1. 找到第二次请求的url，就会获得数据。
   2. 熟悉使用浏览器抓包工具。
   3. F12（检查）的network里头找。
3. 一般来说，是服务器渲染还是客户端渲染，只要`右键看网页源码就能分辨`



### http协议

http协议把一条消息分为三大块内容，无论请求还是相应

请求

```
请求行 -> 请求方式（get / post ） 请求url地址 协议

请求头 -> 放一些服务器要使用的附加消息

请求体 -> 一般放一些请求参数
```



相应

``` 
状态行 -> 协议  状态码（200 / 404 / 500 / 302）

响应头 -> 放一些客户端要使用的一些附加信息

响应体 -> 服务器返回的真正客户端要用的内容（html, json）等
```



请求头中最常见的一些重要内容（爬虫需要）：

1. User-Agent: 请求载体的身份标识（用啥发送的请求） 

2. Referer: 防盗链（这次请求是从哪个页面来的？反爬会用到)
3. cookie: 本地字符串数据信息（用户登录信息，反爬的token)



响应头中一些重要的内容： 

1. cookie: 本地字符串数据信息（用户登录信息，反爬的token)
2. 各种神奇的莫名其妙的字符串（这个需要经验了，一般都是token字样，防止各种攻击和反爬）



请求方式： 

1. GET： 显示提交
2. POST： 隐式提交



### Encoding问题

在python的内存层面，使用的是unicode， 它是不能存储或者传输的

需要将unicode 变成 utf-8  / gbk 这种编码进行存储

```python 
with open('mybaidu.html','w', encoding='utf-8') as f: 
  pass 

# 苹果默认是utf-8, windows默认是gbk
```





## chap2. 数据解析与提取

针对数据在html的情况

解析方式： 

1. re
2. bs4 
3. xpath 



### re解析 

233，见以往的代码

贪婪匹配和惰性匹配（爬虫会用）

```
.* 贪婪
.*? 惰性
```

