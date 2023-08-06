'''

快捷键（默认）
CTRL+; A        执行全部单元测试
CTRL+; E        只执行上次出错的用例
CTRL+; C        清除结果
CTRL+; CTRL+A   调试全部单元测试
CTRL+; CTRL+E   只调试上次出错的用例

'''

# 基础用法 -----------------------------------------------------------------------

import pytest
from beni import bhttp


def test_print():
    print(123)


@pytest.mark.asyncio
async def test_httpGet():
    result, _ = await bhttp.get('https://www.baidu.com')
    assert '<title>百度一下，你就知道</title>' in result.decode()
