import asyncio
import aiohttp 
import os 
import requests 
import json 
import aiofiles

### 现在的盗版视频网站似乎采用了统一的处理流程
### 视频网站的js文件里放index.m3u8    
### index里放真正的m3u8文件
### 视频的url和ts文件的url不对应
### index的url和ts的url对应


# 这个程序还差一个检查文件完整性的东西
# 总共有910个ts,实际上就下载了700个就停止了.


'''分析原因
为什么这个代码下载视频不完整?
- 因为我在下载单个的ts文件中定义的session,包含大量的resp开启和结束,就...
- 可能还有个原因就是读ts m3u8的原因. 这里我直接使用了with来读,而教程里是使用异步读取的.'''
my_header = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
my_proxy = {
    'https': 'https://219.129.167.82:2222'
}
ts_dir = '../videos/'
# url_pre = 'https://v.cdnlz12.com/20240508/13948_3b39707e/2000k/hls/'

url_pre = 'https://v.cdnlz9.com/20240508/24251_d4433e06/2000k/hls/'

async def aiodownload(ts_index,play_index): 
   
    url = url_pre+ts_index
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session: 
        async with session.get(url,headers=my_header) as resp: 
            ts = await resp.content.read()
            async with aiofiles.open(os.path.join(ts_dir,str(play_index)+'.ts'), 'wb') as f: 
                await f.write(ts)


async def read_mixed_m3u8(m3u8_file): 
    with open(m3u8_file, 'r') as f: 
        content = f.readlines()
    tasks = []
    play_index= 0
    for c in content: 
        if c.startswith('#'): 
            continue
        d =aiodownload(c[:-1],play_index)
        play_index +=1 
        tasks.append(asyncio.create_task(d))
    await asyncio.wait(tasks)

if __name__ == '__main__': 
    my_file = './test.m3u8'
    asyncio.run(read_mixed_m3u8(my_file))
    print('done')