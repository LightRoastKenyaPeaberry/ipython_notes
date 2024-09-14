import asyncio
import aiohttp 
import os 
import requests 
import json 
import aiofiles
import re 
from urllib.parse import unquote

my_header = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
def get_first_m3u8(url):
    with requests.get(url,my_header) as resp: 
        page = resp.text
    obj = re.compile(r'var vid="(?P<m3u8>.*?)";', re.S)
    m3u8_url = obj.search(page).group('m3u8')
    # url解码 
    m3u8_url = unquote(m3u8_url)
    # print(m3u8_url)
    return m3u8_url 

def download_m3u8(url, name): 
    with requests.get(url,my_header) as resp: 
        with open(name,'wb') as f: 
            f.write(resp.content)


async def download_ts(ts_url, name, session): 
    async with session.get(ts_url,headers=my_header) as resp: 
        async with aiofiles.open(os.path.join('../911call',name), 'wb') as f: 
            await f.write(await resp.content.read())

    print(f'{name} download!')            

async def aiodownload(ts_pre): 
    tasks = []
    async with aiohttp.ClientSession() as session: # 提前准备好session
        async with aiofiles.open('./m3u8/second.txt','r') as f: 
            async for line in f: 
                if line.startswith('#'): 
                    continue
                line = line.strip() 
                ts_url = ts_pre + line 
                task = asyncio.create_task(download_ts(ts_url,line, session))
                tasks.append(task)
            await asyncio.wait(tasks)

    
if __name__ == '__main__': 
    url = 'https://91mjww.com/vplay/MzM3NjEtMS0w.html'

    first_m3u8 = get_first_m3u8(url)
    download_m3u8(first_m3u8,'./m3u8/first.txt')
    
    # 处理第一个m3u8,获得第二个m3u8文件.
    with open('./m3u8/first.txt', 'r') as f: 
        content = f.readlines() 
    second_m3u8 = first_m3u8.split('index')[0]+content[-1].strip()
    
    download_m3u8(second_m3u8,'./m3u8/second.txt')

    # 下载视频
    ts_pre = second_m3u8.split('mixed')[0]
    
    # 异步下载
    asyncio.run(aiodownload(ts_pre))

    print('\033[1;32m程序完成\n¯\_(ツ)_/¯\033[0m')

