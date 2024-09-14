from threading import Thread   

def func(name):
    for i in range(100): 
        print(name,i)


if __name__ =='__main__': 
    # func() 

    t= Thread(target=func, args=('tami',))  # 创建线程并给它安排任务, 传参必须是元组
    t.start()  # 多线程状态为可以开始工作，具体的执行时间由cpu决定 

    t2= Thread(target=func, args=('lee',))
    t2.start() 


    # for i in range(100): 
    #     print('main',i)



# --------第二种写法---------
# class MyThread(Thread): 
#     def run(self):  # 固定的名字  -- 当线程被执行的时候，被执行的就是run()
#         # some run line 
#         pass 


# if __name__ =='__main__': 
    
#     t= MyThread()
#     # t.run()  这不对， 如果写这个就变成单纯的方法调用，是单线程
#     t.start()  # 正确写法
  

#     for i in range(100): 
#         print('main',i)