# 协程爬虫模板  
import asyncio  
import aiohttp
import os 


urls = ['https://i1.huishahe.com/uploads/tu/201908/9999/1ef009a14b.jpeg',
           'https://i1.huishahe.com/uploads/tu/201903/9999/ab238a6365.jpg',
           'https://i1.huishahe.com/uploads/tu/201903/9999/fd0ed10bba.jpg']
img_dir = './test_dir'
async def download(url): 
    print('开始准备下载')
    name = url.split('/')[-1]
    # s = aiohttp.ClientSession()  # <--> 等价于 requests
    # s.get() or s.post() 
    async with aiohttp.ClientSession() as session: 
        async with session.get(url) as resp: 
            # resp.content.read()  # <--> 等价于 resp.content
            # resp.text() 
            # resp.json() 
            # aiofiles 异步写文件
            with open(os.path.join(img_dir,name), 'wb') as f: 
                f.write(await resp.content.read())
    print('下载完成')

async def main(): 
    
    tasks = [] 
    for url in urls: 
        d= download(url) 
        tasks.append(asyncio.create_task(d)) 
    await asyncio.wait(tasks)

if __name__ == '__main__': 
    asyncio.run(main())