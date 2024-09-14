'''此程序以百度小说为例,爬取内容'''

import asyncio
import aiohttp 
import os 
import requests 
import json 
import aiofiles

my_header = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
book_dir = './test_dir/jouney_to_the_west'

# url : https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4306063500"} --> 所有章节的信息
# https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|1569782244","need_bookinfo":"1"} -->章节内部内容

# 第一个url同步  第二个也就是所有章节的,异步操作

async def aiodownload(bid,cid, title): 
    data = {
        "book_id": bid,
        "cid": bid+'|'+cid, 
        "need_bookinfo": 1
    }
    data = json.dumps(data)
    url = "https://dushu.baidu.com/api/pc/getChapterContent?data="+data
    async with aiohttp.ClientSession(headers=my_header) as session: 
        async with session.get(url) as resp: 
            dic = await resp.json()
            async with aiofiles.open(os.path.join(book_dir,title), 'w', encoding='utf-8') as f: 
                await f.write(dic['data']['novel']['content'])

    # pass 

async def get_catalog(url): 
    with requests.get(url,headers=my_header) as resp: 
        content = resp.json()
        book_id = content['data']['novel']['book_id']
        chapter_info  = content['data']['novel']['items']
        # titles= []
        # cids = []
        tasks = []
        for c in chapter_info: 
            title= (c['title'])
            cid=c['cid']
            # 在这里异步
            tasks.append(asyncio.create_task(aiodownload(book_id,cid,title)))
        await asyncio.wait(tasks)



if __name__ == '__main__': 
    book_id = '4306063500'
    url =  'https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"'+book_id+'"}'
    
    asyncio.run(get_catalog(url)) 
    print('done')