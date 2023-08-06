# ascall

> ascall用于自动识别同步或异步的可调用对象，
> 然后进行转换并执行异步调用返回结果。
> 
> ascall可作为函数运行，也可作为装饰器。

## 装饰器用法

```python
import asyncio
from ascall import ascall


@ascall()
def sync_func():
    print("sync func run.")


asyncio.run(sync_func())
```

## 函数用法

```python
import asyncio
from ascall import ascall


def sync_func(msg: str):
    print("sync func run.", msg)


async def main():
    print("async func run.")
    await ascall(sync_func, "some msg")


asyncio.run(main())
```