from hashlib import md5 
import json 
# a = PC42ce3bfa4980a9

# h = o = n()(a).substring(16)

# n() --> md5 

def md5_result(text):
    m5= md5() 
    m5.update(text.encode('utf-8'))
    return m5.hexdigest() 

# res = md5_result('PC42ce3bfa4980a9')
# print(res[:16]) 

# res = a2eb17f65d6f4b3f
#       a2eb17f65d6f4b3f

appCode= "PC42ce3bfa4980a9"

e = '/v1/threads/list/df'
param = "{\"fid\":\"598\",\"showUnAnswer\":1,\"typeId\":5,\"lastItem\":\"19302878\",\"position\":\"0\",\"rows\":10,\"orderType\":2}"

param = json.loads(param)
# print(param)
param = json.dumps(param)
# print(param.replace(' ', ''))

i = e+param.replace(' ', '')+md5_result(appCode)[:16]

# print(i)
res = md5_result(i)

print(res)