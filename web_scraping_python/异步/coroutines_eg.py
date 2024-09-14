import asyncio
import time 



# async def func(): 
#     print('hi, my name is zz')


# if __name__ == '__main__': 
#     # func() #  此时的函数是异步协程函数,此时函数执行得到的是一个协程对象
#     g= func() 
#     # print(g)
#     asyncio.run(g)


async def func1():
    print('My name is a')
    # time.sleep(2)   # 当程序出现同步操作, 异步就中断了
    await asyncio.sleep(2)  # await需要放在async函数中,挂起操作放在协程对象前
    print('My name is a')

async def func2():
    print('My name is b')
    # time.sleep(3)
    await asyncio.sleep(3)
    print('My name is b')

async def func3():
    print('My name is c')
    # time.sleep(4)
    await asyncio.sleep(4)
    print('My name is c')


# if __name__ == '__main__': 
#     f1 = func1() 
#     f2 = func2() 
#     f3 = func3() 

#     tasks = [f1, f2, f3]
#     t1 = time.time() 
#     asyncio.run(asyncio.wait(tasks))
#     t2 = time.time() 
#     print(t2-t1)


# python官方推荐写的
async def main(): 
    # 写法一 不推荐 
    # f1 = func1()
    # await f1

    # 写法2 
    tasks  = [asyncio.create_task(func1()),
              asyncio.create_task(func2()),
              asyncio.create_task(func3())]
    await asyncio.wait(tasks)

if __name__ =='__main__': 
    t1= time.time()
    asyncio.run(main())
    t2 = time.time() 
    print(t2-t1)