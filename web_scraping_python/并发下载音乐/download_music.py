'''
针对freemp3这个网站做的爬虫
使用了线程池
指定 `歌手名` `爬取页数` 进行爬取
效果: 在执行程序的该路径创建歌手路径,其中包含以歌曲名的目录.

需要进一步优化的点: 网易的许多url都404了,对于404的歌曲没必要保存了,直接删除目录.
'''

import requests 
from queue import Queue 
import os 
from queue import Empty
from concurrent.futures.thread import ThreadPoolExecutor

class MP3Spider: 
    def __init__(self, name): 
        self.url = 'https://www.myfreemp3.com.cn'
        self.post_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.get_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }

        self.name = name 
        # self.page = page 
        self.music_list_queue = Queue() 
        self.download_url_queue = Queue() 

        # 创建歌手的目录
        if not os.path.exists(name):
            os.mkdir(f'./{name}')


    def get_music_list(self, page): 
        params = {
            "input": self.name,
            "filter": "name",
            "page": page,
            "type": "netease"
        }
        with requests.post(url=self.url,data=params, headers=self.post_headers) as resp: 
            # print(resp.json())
            # result  = resp.json() 
            self.music_list_queue.put(resp.json()['data']['list'])

    def parse_result(self): 
        while True: 
            try:
                result = self.music_list_queue.get(timeout=10) 
            except Empty: 
                print('the singer pages are to the end or timeout.')
                break
            for item in result: 
                self.download_url_queue.put((item.get('author'),item.get('title'),item.get('url'), item.get('lrc'), item.get('pic')))

    def save_data(self): 
        while True: 
            try:
                authour, title, url, lrc, pic = self.download_url_queue.get(timeout=10)
                if os.path.exists(os.path.join(self.name,title)): 
                    continue
                song_root = os.path.join(self.name,title)
                os.mkdir(song_root)
            except Empty: 
                print('the music list is empty') 
                break 

            with open(os.path.join(song_root,"lyr.txt"), 'w') as f: 
                f.write(lrc)

            with requests.get(pic,headers=self.get_headers) as resp: 
                with open(os.path.join(song_root,'cover.jpg'), 'wb') as f: 
                    f.write(resp.content)
            
            with requests.get(url,headers=self.get_headers) as resp: 
                # netease 404 page 
                '''
                    _________________________________________________
            /|     |                                                 |
            ||     |                                                 |
       .----|-----,|             here!                               |
       ||  ||   ==||                                                 |
  .-----'--'|   ==||                                                 |
  |)-      ~|     ||_________________________________________________|
  | ___     |     |____...==..._  >\______________________________|
 [_/.-.\"--"-------- //.-.  .-.\\/   |/            \\ .-.  .-. //
   ( o )`==="""""""""`( o )( o )     o              `( o )( o )` 
    '-'                '-'  '-'                       '-'  '-'
                '''
                if resp.headers.get('Content-Type').startswith('text'):
                    continue
                with open(os.path.join(song_root,f'{authour}_{title}.mp3'), 'wb') as f: 
                    f.write(resp.content)

            print(f'{title} done!')



if __name__ == "__main__": 
    mm = MP3Spider('adele')
    
    with ThreadPoolExecutor(max_workers=8) as tp: 
        for i in range(1,2):
            tp.submit(mm.get_music_list(i))
        tp.submit(mm.parse_result())
        tp.submit(mm.save_data())
        tp.submit(mm.save_data())
        tp.submit(mm.save_data())

    print('\033[1;32m程序完成\n¯\_(ツ)_/¯\033[0m')