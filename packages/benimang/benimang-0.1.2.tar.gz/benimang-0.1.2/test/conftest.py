'''
快捷键（默认）
CTRL+; A        执行全部单元测试
CTRL+; E        只执行上次出错的用例
CTRL+; C        清除结果
CTRL+; CTRL+A   调试全部单元测试
CTRL+; CTRL+E   只调试上次出错的用例
'''

import nest_asyncio
import pytest


@pytest.fixture(scope='session', autouse=True)
def prepareSession():
    nest_asyncio.apply()
    print('session before')
    yield
    print('session after')
