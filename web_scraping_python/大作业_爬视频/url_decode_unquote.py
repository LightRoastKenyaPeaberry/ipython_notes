from urllib.parse import unquote

url = 'https://www.xfz.cn/api/website/articles/?p=1&n=20&type=%E8%9E%8D%E8%B5%84%E6%B6%88%E6%81%AF'

res = unquote(url)

print(res)