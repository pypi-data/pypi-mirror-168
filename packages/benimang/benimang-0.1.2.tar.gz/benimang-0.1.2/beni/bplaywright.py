import os
from contextlib import asynccontextmanager
from typing import Any, cast

from playwright.async_api import async_playwright
from playwright.sync_api import BrowserContext, sync_playwright

from beni import bpath

_testContext: BrowserContext | None = None


def test(*, url: str = '', storage_state: str | None = None):
    global _testContext
    if not _testContext:
        import nest_asyncio
        nest_asyncio.apply()
        os.environ['PWDEBUG'] = 'console'
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False, channel='chrome')
        _testContext = browser.new_context(storage_state=cast(str, storage_state))
    page = _testContext.new_page()
    if url:
        page.goto(url)
    return page


def testStorageState():
    if _testContext:
        _testContext.storage_state(path=bpath.getDesktop('storage_state.dat'))


@asynccontextmanager
async def page(
    *,
    browser: dict[str, Any] = {},
    context: dict[str, Any] = {},
    page: dict[str, Any] = {},
):
    '''
    ```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    },
    context={
        'storage_state': FILE_STATE,
    },
    ```
    '''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            async with await b.new_context(**context) as c:
                async with await c.new_page(**page) as p:
                    yield p


@asynccontextmanager
async def context(
    *,
    browser: dict[str, Any] = {},
    context: dict[str, Any] = {},
):
    '''
    ```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    },
    context={
        'storage_state': FILE_STATE,
    },
    ```
    '''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            async with await b.new_context(**context) as c:
                yield c


@asynccontextmanager
async def browser(
    *,
    browser: dict[str, Any] = {},
):
    '''
    ```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    }
    ```
    '''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            yield b
