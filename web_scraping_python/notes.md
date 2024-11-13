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



## 模拟登陆 

### cookie+session鉴权



### 基于token鉴权



一般来说如果登录的时候, post携带的是form data, 90%的可能cookie+session

如果携带的是json( resquest payload), 登录域名不一样, 大概率是token



1. 使用cookie+seesion鉴权的网站模拟登录的流程
   1. 传递账号密码，进行登录
   2. 登录之后保cookie(返回时在啊应头的set-cookie字段中)
   3. 请求其他的页面时，携带cookie
2. 使用token鉴权的网站桃拟登录的流图
   1. 传递账号密码，进行登录
   2. 登录之后保token(返回的时候，在啊应体中)
   3. 请求其他的页面时，携带token(手动)



## 反爬手段

- user-agent 
- 防盗链 检测请求的来源 referer
- 政府网站的`创宇盾`
- 请求头(post)里的X-Requested-With: XMLHttpRequest



## selenium 

是一个web自动化测试工具,最初是为了网站自动化测试而开发的,可以按照指定的命令自动操作. 它可以直接运行在浏览器上,支持所有主流浏览器

```python
from selenium import webdriver
import time 

# 1. selenium打开浏览器
driver = webdriver.Chrome() 

# 2. 打开要操作的页面
url = 'some url'
driver.get(url)

time.sleep(10)
# 3. 获取页面的数据

html = driver.page_source
print(html)

# 关闭浏览器
driver.quit()
```

```python
# other actions

driver.maximize_window()

driver.refresh() 

driver.save_screenshot('test.png')
```

### driver对象相关属性

- current_url
- title
- page_source 
- current_window_handle



### 元素定位

**可以By许多种方式,最推荐xpath**

```python
from selenium.webdriver.common.by import By

ele = driver.find_element(By.XPATH, '<//input[@id="sb_from_q"]>')

ele.set_keys('深度学习')
```

### 元素属性和操作

**属性**

- tagname
- text
- parent
- get_attribute() 
- s_displayed() 判断元素是否可见

**操作**

- click()
- send_keys() 输入内容
- clear()  清空表单

### 等待机制

现在的网页很多都是动态加载的，如果页面的内容发生了改变，就需要时间来渲染，代码是自动执行的，有可能你在执行的时候新的元素还没加载出来，就查找不到，报no such element的错误。如果报这个错误，很有可能定位表达式不对，或者是页面元素已经发生变化。

**等待的三种方式** 

- 强制等待 time.sleep(3)
- 隐式等待 driver.implicitly_wait(10) 
  - 如果页面找某个元素,在10秒内加载出来,就继续执行,否则报错
- 显式等待(明确等待的条件)
  - 条件比如: 等到元素可见, 元素可点击



### iframe切换 

**切换到指定的iframe中**

```python 
# way 1 the name of iframe 
driver.switch_to.frame('login_frame')

# way 2 element 
ele_iframe = driver.find_element_by_xpath('//iframe[@id="login_frame"]')

driver.switch_to.frame(ele_iframe)

# way 3 index 
driver.switch_to.frame(1)
```



**切回默认html页面** 

```python
driver.switch_to.default_content() 
```



**切换到父级的iframe中** 

```python
driver.switch_to.parent_frame() 
```



### 窗口滚动

元素属性: `location_once_scrolled_into_view`

### js脚本执行

#### js滚动窗口

```python
js = "window.scrollTo(x=0,y,500)"
driver.execute_script(js) 


# 相对当前位置滚动 
js = "window.scrollBy(x=0,y,500)"
```



### 鼠标操作

```python
from selenium.webdriver import ActionChains
```

- click
- double_click
- context_click
- move_to_element
- click_and_hold
- move_by_offset 
- drag_and_drop
- release 
- perform 

### 伪装(浏览器特征检测)

**selenium启动的浏览器可能具有一下特殊的特征**

- User-Agent 
- 自动化工具标识 `X-Requested-With`, `DNT`
- WebDriver相关属性: 在全局`window`对象中注入特定的属性, e.g. `webdriver`, `navigator.webdriver`
- 页面加载行为: 快速点击, 快速输入文本
- 元素检测: 在DOM中插入一些特定的元素或属性用于控制浏览器行为,可以检测这些元素的属性是否被触发来判断是否为selenium打开的浏览器

**应对之策**

- `--disable-infobars`
- `excludeSwitches`, `enable-automation` 
- `useAutomationExtension: False`
- `page.addScriptToEvaluateOnNewDocument`, 可以在每次页面加载时执行指定的JavaScript代码。我们每次打开新页面之前执行`hide.js`来隐藏selenium启动浏览器生成的属性，从而防止被检测出来时爬虫。

**在网上下载了一个stealth.min.js文件,能绕过反爬检测** 

笔趣阁的登录会跳出一个中间真人检测页面,selenium不能通过

只好伪装

[csdn给的三种方法](https://blog.csdn.net/weixin_45081575/article/details/126585575)

[mac selenium 接管浏览器教程](https://www.cnblogs.com/csubcc/p/15728380.html)

## js逆向分析 

### node.js 

`pip install pyexcejs`

imac的spider环境没有支持版本, macbook有.

**如果遇到非常复杂的加密算法,直接将js代码复制过来,按照这个流程调用即可.**

```python
import execjs 


js_code = '''
function add(a,b) {
    return a+b 
}

function work() {
    return 'python233'
}
'''

# 1. compile
JS = execjs.compile(js_code)

# 2. call 
res = JS.call('add',1,2)
print(res)

res = JS.call('work')
print(res)
```

### 案例

- 领导留言板
- 去哪儿网

### 验证码

打码平台

### 反调试

反调试技术是指通过avaScript代码，在网页加载时检测是否处于调试环境，并采取措施阻止调试器的使用，使得调试变得困难或无法进行。

**常见反调试技术**

- **禁用调试快捷键**：禁用鼠标右键，禁用快捷键F12,无法打开调试控制台
- **检测调试器工具**：通过检测调试器工具的存在来判断是否处于调试环境。
- **检测浏览状态**：通过监测浏览器状态的变化，来判断是否处于调试环境。
- **模糊代码**：对关键代码进行混淆或加密，使得难以理解和分析。
- **定时检测**：定时检测调试器状态，如果检测到调试器存在，则执行相应的反调试代码。

#### 案例

**通过debugger断定定时递归实现无限反调试**

```js 
function Debugging() {
  debugger 
  setInterVal(Debugging, 1000);
}
Debugging();
```



**控制台自动清屏,干扰console.log调试** 

```js
function startClearConsole(){
  setInterval(function() {
    console.clear();
  },1000);
}
startClearConsole();
```





## Cookie池和ip代理

### 代理

花钱买一些.然后在代码里使用random.choice,在每次请求前随机获取一个ip.



### cookie 

**带上cookie的好处**

- 能够访问登录后的页面
- 实现部分的反 反爬

**弊端**

- 一套cookie往往对应一个用户的信息,请求太频繁也有可能别识别为爬虫
  - 登录: 多账号登录,保存cookie
  - 未登录: 多启动几个浏览器复制 / 复制完清空cookie再请求



### cookie池搭建

还是一个list, random.choice.



### cookie+ip池封装

每个cookie搭配一个ip



## 字体反爬 

如果指定了字体, 那么在输入字符后,在输出到网页前,会查找字体文件找到对应的字形,将字形输出.

所以说,如果网页做了反爬处理,那么,在html内容里,是加了密的字符,这些字符在字体文件中对应的`字形才是真正的信息`.

```
# 字体文件
0 - hex(unicode(xxxx))
1 -
2 -
3 -
4 -
5 -
...
```

```python
cha = '我'

# unicode 
uni_cha = ord(cha)

# hex
hex_cha = hex(uni_cha)

# uncode --> char
print(chr(uni_cha))
```

页面显示前做的事

1. 将字符转换为16进制下的unicode
2. 在字体文件中找到对应的字形
3. 将字形绘制到页面上

### 解法

1. 通过抓包找到字体文件,解析字体文件

```python
!pip install fontTools
```

2. 构建字典, 无意义的字符是键, 有意义的字形是值. 值的识别用ocr.
3. 在html内容里替换.

## 杂记

### json

json.loads  将json字符串转化为python数据结构(dict / list)

json.dumps 将python数据结构(dict / list)转化为json字符串



json.load 从json文件中读取数据并转换为python对象

json.dump 将python数据结构 写到 json文件中



### jsonpath

| expr        | desc                   |
| ----------- | ---------------------- |
| `$`         | 根节点                 |
| `.` or `[]` | 子节点                 |
| `..`        | 子孙节点               |
| `[]`        | 数组下标, 根据内容选值 |



### 合并视频音频

虽然python有包,但其实就是调用了ffmpeg.

```shell
ffmpeg -i a.mp4 -i b.mp4 -c copy 'output.mp4'
```

