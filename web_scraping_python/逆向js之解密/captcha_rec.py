'''
超级鹰: https://www.chaojiying.com/user/login/
图片验证码识别.
表单参数: 
{
user: test
pass: test
imgtxt: 2333
act: 1
}
由于每次请求,验证码都会变化,所以在session内执行.
步骤: 
1. 发送请求拿到验证码图片

2. 识别验证码的内容
3. 发送登录请求
'''
import requests 
from requests import session
import ddddocr 


s = session() 
login_url = 'https://www.chaojiying.com/user/login/'
captcha_url = 'https://www.chaojiying.com/include/code/code.php?u=1'
my_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

ocr = ddddocr.DdddOcr() 


# 拿到验证码, 送入ocr识别
with s.get(captcha_url,headers=my_headers) as resp: 
    text = ocr.classification(resp.content)
    with open('./captcha.png', 'wb') as f: 
        f.write(resp.content)

print(text)

my_params = {
    "user": "marryyoo",
    "pass": "marryyoois111.",
    "imgtxt": text,
    "act": 1
}
# 登录
with s.post(login_url, data=my_params) as resp: 
    print(resp.text)




