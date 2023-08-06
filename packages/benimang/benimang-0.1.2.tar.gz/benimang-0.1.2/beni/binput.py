import asyncio
import getpass
import random
from typing import Any, Callable, Coroutine, cast

import aioconsole

from beni import bcolor


async def hold(msg: str | None = None, password: bool = False, *exitvalue_list: str):
    msg = msg or '测试暂停，输入exit可以退出'
    msg = f'{msg}: '
    exitvalue_list = exitvalue_list or ('exit',)
    while True:
        if password:
            inputValue = getpass.getpass(msg)
        else:
            inputValue = cast(str, await aioconsole.ainput(msg))
        if (inputValue in exitvalue_list) or ('*' in exitvalue_list):
            return inputValue


async def confirm(msg: str = '确认'):
    code = f'{random.randint(1, 999):03}'
    await hold(f'{msg} [ {_getRemindMsg(code)} ]', False, code)


async def select(*data: tuple[str, str, str | Callable[[str], Any] | None, Callable[[str], Coroutine[Any, Any, Any]] | None]):
    '''
    value = goSelect(
        ('descA', 'confirmDescA', 'quanbuqueren', __handlerA),
        ('descB', 'confirmDescB', lambda x: ..., __handlerB),
    )
    '''
    print()
    print('-' * 30)
    print()
    for msg, inputDisplay, _, _ in data:
        if inputDisplay:
            msg += f' [ {_getRemindMsg(inputDisplay)} ]'
        print(msg)
    print()
    while True:
        value = cast(str, await aioconsole.ainput('输入选择：'))
        isMatch = False
        result = None
        for msg, inputDisplay, inputValue, handler in data:
            inputValue = inputValue or inputDisplay or msg
            if type(inputValue) is str:
                isMatch = value == inputValue
            else:
                try:
                    isMatch = cast(Callable[[str], bool], inputValue)(value)
                except:
                    pass
            if isMatch:
                if handler:
                    result = asyncio.run(handler(value))
                    break
        if isMatch and result is not False:
            return value


async def inputCheck(msg: str, check: Callable[[str], Any]):
    while True:
        try:
            value = cast(str, await aioconsole.ainput(f'{msg}：'))
            if check(value):
                return value
        except:
            pass


def _getRemindMsg(msg: str):
    return bcolor.yellow(msg)
