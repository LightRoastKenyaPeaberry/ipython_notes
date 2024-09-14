from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def fn(name): 
    for i in range(100): 
        print(name,i)

if __name__ =='__main__': 
    # 创建有50个线程的线程池 
    with ThreadPoolExecutor(50) as t: 
        for i in range(200): 
            t.submit(fn,name=f'线程{i}')

            
    print('over')
