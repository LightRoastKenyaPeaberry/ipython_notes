# python异步

## asyncio 

本质还是单进程单线程

比较适合需要等待的任务,比如网络通讯

核心: eventloop

corountine & task 

Coroutine funciton & coroutine object 

所有的`async def`都是coroutine function,被调用时会返回coroutine object

如何真正运行这个函数? 

1. 进入async模式-->  `asyncio.run(<async func>) `
2. 将coroutine变成task --> `await` or `asyncio.create_task,  await`

