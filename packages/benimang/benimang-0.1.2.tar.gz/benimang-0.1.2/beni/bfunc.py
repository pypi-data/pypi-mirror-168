import asyncio
import binascii
import hashlib
import json
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar, cast

import async_timeout

Fun = TypeVar("Fun", bound=Callable[..., object])
AsyncFun = TypeVar("AsyncFun", bound=Callable[..., Coroutine[Any, Any, object]])
AnyType = TypeVar("AnyType")


def jsonDumpsMini(value: Any):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def md5Bytes(data: bytes):

    return hashlib.md5(data).hexdigest()


def md5Str(content: str):
    return md5Bytes(content.encode())


def md5Data(data: Any):
    return md5Str(
        jsonDumpsMini(data)
    )


def crcBytes(data: bytes):

    return hex(binascii.crc32(data))[2:].zfill(8)


def crcStr(content: str):
    return crcBytes(content.encode())


def crcData(data: Any):
    return crcStr(
        jsonDumpsMini(data)
    )



IntFloatStr = TypeVar("IntFloatStr", int, float, str)


def getValueInside(value: IntFloatStr, minValue: IntFloatStr, maxValue: IntFloatStr):
    '包括最小值和最大值'
    value = min(value, maxValue)
    value = max(value, minValue)
    return value


def getPercentValue(targetValue: float, minValue: float, maxValue: float, minResult: float, maxResult: float):
    '''
    根据百分之计算指定数值
    '''
    if targetValue >= maxValue:
        return maxResult
    elif targetValue <= minValue:
        return minResult
    else:
        percent = (targetValue - minValue) / (maxValue - minValue)
        return minResult + (maxResult - minResult) * percent


def getIncrease(fromValue: float, toValue: float):
    return toValue / fromValue - 1



def toFloat(value: IntFloatStr, default: float = 0):
    result = default
    try:
        result = float(value)
    except:
        pass
    return result


def toInt(value: IntFloatStr, default: int = 0):
    result = default
    try:
        result = int(value)
    except:
        pass
    return result

def retry(times: int):
    def fun(func: AsyncFun) -> AsyncFun:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            current = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except:
                    current += 1
                    if current >= times:
                        raise
        return cast(AsyncFun, wrapper)
    return fun


@asynccontextmanager
async def timeout(timeout: float):
    async with async_timeout.timeout(timeout):
        yield




def initErrorFormat():
    import pretty_errors
    pretty_errors.configure(
        separator_character='*',
        filename_display=pretty_errors.FILENAME_COMPACT,
        # line_number_first   = True,
        display_link=True,
        lines_before=5,
        lines_after=2,
        line_color=pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
        code_color='  ' + pretty_errors.default_config.line_color,
        truncate_code=False,
        display_locals=True
    )
    # pretty_errors.blacklist('c:/python')


def Counter(value: int = 0):
    def _(v: int = 1):
        nonlocal value
        value += v
        return value
    return _


class TaskList():

    def __init__(self):
        self._enabled = True
        self._list: list[Coroutine[Any, Any, Any]] = []

    async def add(self, task: Coroutine[Any, Any, Any]):
        assert self._enabled
        asyncio.create_task(task)
        self._list.append(task)

    async def waitAll(self):
        self._enabled = False
        await asyncio.gather(*self._list)
