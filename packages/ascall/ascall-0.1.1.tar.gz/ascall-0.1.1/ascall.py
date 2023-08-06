# coding=utf-8
"""
ascall用于自动识别同步或异步的可调用对象，然后进行转换并执行异步调用返回结果。
"""

__version__ = "0.1.1"

__all__ = ["ascall"]


import asyncio
import functools
from typing import Callable


class AsCall:
    """ascall用于自动识别同步或异步的可调用对象，然后进行转换并执行异步调用返回结果。
    ascall可作为函数运行，也可作为装饰器。
    """
    def __init__(self, call: Callable = None, *args, **kwargs):
        self.call = call
        self._func_coroutine = None  # 存放装饰的异步函数协程对象
        if self.call:
            self.set_func_coroutine(*args, **kwargs)

    def set_func_coroutine(self, *args, **kwargs):
        assert callable(self.call), f"{self.call} 必须是可调用对象。"
        if asyncio.iscoroutinefunction(self.call):
            self._func_coroutine = self.call(*args, **kwargs)
        else:
            self._func_coroutine = asyncio.to_thread(self.call, *args, **kwargs)

    async def run_func(self):
        """用于__await__执行"""
        return await self._func_coroutine

    def __await__(self):
        """
        必须定义这个方法才能直接 await 这个类的对象
        并且，返回值必须是一个 iterator，这里直接
        使用 async 函数的内置方法 __await__()
        """
        return self.run_func().__await__()

    def __call__(self, func):
        """同步函数装饰器: 装饰同步函数
        """

        @functools.wraps(func)
        async def func_magic_async(*args, **kwargs):
            assert not self.call, f"使用 @{self.__class__.__name__}() 则不允许传 call 参数。"
            self.call = func
            self.set_func_coroutine(*args, **kwargs)
            await self
        return func_magic_async


ascall = AsCall
