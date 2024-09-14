from multiprocessing import Process 
import time 


def func():
    for i in range(100): 
        print('子进程',i)

if __name__ =='__main__':
    p = Process(target=func)
    p.start() 

    # time.sleep(0.1)

    for i in range(100):
        print('主进程',i)
