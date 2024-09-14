import requests 
from concurrent.futures import ThreadPoolExecutor
import csv 

my_url = 'https://movie.douban.com/j/chart/top_list'

my_headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def download_one_page(start): 
    start= str(start)
    my_params = {
    "type": "16",
    "interval_id": "100:90",
    "action": "",
    "start": start,
    "limit": "20"
    }

    try: 
        resp = requests.get(my_url,params=my_params,headers=my_headers)
    except requests.exceptions.RequestException as e:
        print(f'page {start} error: {e}')
        pass 
    else: 
        # print(resp.json()) 
        items = resp.json() 
        resp.close() 

        f= open('./test_dir/movies_fantasy.csv','a') 
        csvwriter= csv.writer(f)

        for i in items: 
            record = [i['title'],i['score']]
            # print(record)
            csvwriter.writerow(record)
        f.close() 
        print(f'page {start} done!')

# download_one_page(20) 
if __name__ == '__main__': 
    with ThreadPoolExecutor(20) as t: 
        for i in range(0,232,20): 
            t.submit(download_one_page,i)
    
    print('all done!')
