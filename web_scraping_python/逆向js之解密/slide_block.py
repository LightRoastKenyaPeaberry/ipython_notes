'''
去哪儿网站的登录
'''
import time 
import random 
import json 
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad 
import base64
import requests 
from requests import session

'''
track: 
['35489;273.00;407.00;0.00', 
'35565;273.00;407.00;0.00', 
'35586;274.00;407.00;1.00', 
'35608;291.00;405.00;18.00', 
'35631;323.00;403.00;50.00', 
'35655;364.00;403.00;91.00', 
'35677;418.00;403.00;145.00', 
'35699;477.00;403.00;204.00', 
'35721;546.00;405.00;273.00', 
'35743;598.00;409.00;325.00', 
'35766;653.00;413.00;380.00', 
'35788;695.00;416.00;422.00']
'''

# my_headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
# }

# def get_uid(s): 
#     url = 'https://user.qunar.com/passport/login.jsp'
#     resp = s.get(url,headers=my_headers)
#     return resp.cookies['QN1']
    
    


def get_track(st):
    st = st+random.randint(100,200)
    t = int(str(st)[-5:])

    x = 273.0
    y= 407.0

    # 滑动总宽度 
    width = random.randint(422,438)

    increment = 0
    track = []  # [time, x, y , x_increment]
    track.append(f'{t};{x:.2f};{y:.2f};{increment:.2f}')

    while increment < width: 
        st= st+random.randint(10,40)
        t= int(str(st)[-5:]) 

        delta_x= random.randint(10,70)
        increment += delta_x
        x += delta_x

        if increment > width: 
            temp = increment
            increment = width
            x -= temp - increment 

        track.append(f'{t};{x:.2f};{y:.2f};{increment:.2f}')

    return track        

    # print(track)
    # for t in track: 
    #     print(t)
    # print(len(track))

def get_params(): 
    '''
    注意加密需要的是json字符串.
    '''
    ot= int(time.time()*1000)
    st = ot + random.randint(1000,1500)
    track = get_track(st)
    et= st + random.randint(500,1000)
    deviceMotion = [{"isTrusted":True} for i in range(len(track))]
    # uid是写在cookie中的.
    params = {
        'acc': [],
        'deviceMotion': deviceMotion,
        'openTime': ot,
        'startTime': st,
        'ori': [],
        'track': track,
        'uid': '00010c803068651d53d8f0cc',
        'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'endTime': et
    }

    return json.dumps(params)
    

def aes_en(content, en_key):
    '''
    content: json string content to be ciphered
    en_key: ...
    both of them have to be encoded in utf-8'''
    en_key = en_key.encode('utf-8')

    aes = AES.new(
        key=en_key,
        mode = AES.MODE_ECB
    )
    content = pad(content.encode('utf-8'), 16)
    
    cip_content = aes.encrypt(content)
    cip_content = base64.b64encode(cip_content)
    return cip_content.decode()
    



# pp = get_params() 
# # print(pp)

# # # en_key : 227V2xYeHTARSh1R

# res = aes_en(pp,'227V2xYeHTARSh1R')
# # print(res)

# # request payload 
# my_param = {
#     "appCode": "register_pc",
#     "cs": "pc", 
#     "data": res,
#     "orca": 2
# }


if __name__ == '__main__': 
    # 第一阶段,通过滑动验证码
    url = 'https://vercode.qunar.com/inner/captcha/snapshot'
    pp = get_params() 
    en_key = '227V2xYeHTARSh1R'
    res =aes_en(pp,en_key)
    my_param = {
    "appCode": "register_pc",
    "cs": "pc", 
    "data": res,
    "orca": 2
    }
    my_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://user.qunar.com/",
    "Cookie": "QN1=00010c803068651d53d8f0cc; QN300=s%3Dbing; QN99=3019; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN205=s%3Dbing; QN277=s%3Dbing; QN267=1452706681d94a22de; csrfToken=9tJU22rNwcwpG4BwPrh2lpXsjFYMUeFz; QN269=294FE530772211EF98C01A0845F00B18; QN601=18314f90f9fa610584857ede9be47aa2; _i=ueHd8p0HzwyXC6bXd0hP5U7y5MWX; _vi=BKZyjuNJwVeEM4TovhcUrfGieRz7vVN6PTzQapmPZhuvlHXlH8t2k_yprRoYoVfxjIr67vVhGLYpRoGauM51k5He5TP-GopcxwEsfTYJPMSsafiXk97OvEmlNr97g5Cyi-UBeyIr_PrE1-uSUao2O2jri9jVDnN2_iCErMcwH426; QN48=0000f3002f10651d5400176e; quinn=2a7bc27294b1a7492772c4cbec2db1169fb0e159ee2958d2a79a6891ddaf9e672ff9a7a4b0e447153ed52819f3a9b3d2; ctt_june=1683616182042##iK3wWRPmWwPwawPwa%3D3na%3DGGVKfIaRWIEDWIWRv%3DVPGTERXsXKjsX%3DaAVPXAiK3siK3saKgwWStnWsXnVKDmWUPwaUvt; QN271AC=register_pc; ariaDefaultTheme=undefined; ctf_june=1683616182042##iK3waKX%3DawPwawPwaskIXKt%2BXKEGESHRXsGIX2EDaRDmXskDX%3Da%3DWDkhXStNiK3siK3saKgwWStsaR2%3DVRv%2BVuPwaUvt; QN271SL=22c5b8ba6893431e06aa7e5b3e5358a4; QN271RC=22c5b8ba6893431e06aa7e5b3e5358a4; cs_june=fea26da18ab66061d3f639f14eb19a89566b00fc0f217b9539bc8b45b9a125668bd9acc5f6f9f31bdf66a613c5a2cfb5c4af5ca54e0dc881e1c71f3c47c7d8a7b17c80df7eee7c02a9c1a6a5b97c1179315e7df5bccb28e74ad41e30dfebe6c75a737ae180251ef5be23400b098dd8ca"
    }
    s = session()
    with s.post(url,json=my_param,headers=my_headers) as resp: 
        snapshot_res = resp.json()
    
    # 第二阶段,通过手机验证码
    url2= 'https://user.qunar.com/weblogin/sendLoginCode'
    my_headers2 = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://user.qunar.com/passport/login.jsp?ret=https%3A%2F%2Fflight.qunar.com%2F",
    }    

    my_param2= {
    "usersource": "",
    "source": "",
    "ret": "https://flight.qunar.com/",
    "ref": "",
    "business": "",
    "pid": "",
    "originChannel": "",
    "activityCode": "",
    "origin": "",
    "mobile": 19966486928,
    "prenum": 86,
    "loginSource": 1,
    "slideToken": snapshot_res['data']['cst'],
    "smsType": 0,
    "appcode": "register_pc",
    "bella": "1683616182042##aa61064fe5832cf99c7129850219a38ebc406ad0",
    "captchaType": ""
    }
    with s.post(url2,data=my_param2,headers=my_headers2) as resp: 
        print(resp.json())


    # 登录

    url3 = 'https://user.qunar.com/weblogin/verifyMobileVcode'
    vcode= input('your code: ')
    my_param3 = {
    "activityCode": "",
    "appcode": "register_pc",
    "business": "",
    "captchaType": "",
    "loginSource": 1,
    "mobile": "19966486928",
    "originChannel": "",
    "piccoloT": "login_register_pc",
    "pid": "",
    "prenum": "86",
    "ref": "",
    "ret": "https://flight.qunar.com/",
    "slideToken": snapshot_res['data']['cst'],
    "source": "",
    "type": "3",
    "usersource": "",
    "vcode": vcode
    }
    my_headers3 = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Referer": "https://user.qunar.com/passport/login.jsp?"
    }

    with s.post(url3,json=my_param3,headers=my_headers3) as resp: 
        print(resp.json())