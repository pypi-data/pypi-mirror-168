from pathlib import Path
from typing import Any

import aiofiles

from beni import bfunc, block, bpath

_limit = 50


@block.limit(_limit)
async def writeText(file: Path | str, content: str, encoding: str = 'utf8', newline: str = '\n'):
    if type(file) is not Path:
        file = bpath.get(file)
    bpath.make(file.parent)
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        return await f.write(content)


@block.limit(_limit)
async def writeBytes(file: Path | str, data: bytes):
    if type(file) is not Path:
        file = bpath.get(file)
    bpath.make(file.parent)
    async with aiofiles.open(file, 'wb') as f:
        return await f.write(data)


@block.limit(_limit)
async def writeYaml(file: Path | str, data: Any):
    import yaml
    await writeText(file, yaml.safe_dump(data))


@block.limit(_limit)
async def writeJson(file: Path | str, data: Any, mini: bool = True):
    if mini:
        await writeText(file, bfunc.jsonDumpsMini(data))
    else:
        import json
        await writeText(file, json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))


@block.limit(_limit)
async def readText(file: Path | str, encoding: str = 'utf8', newline: str = '\n'):
    async with aiofiles.open(file, 'r', encoding=encoding, newline=newline) as f:
        return await f.read()


@block.limit(_limit)
async def readBytes(file: Path | str):
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()


@block.limit(_limit)
async def readYaml(file: Path | str):
    import yaml
    return yaml.safe_load(
        await readText(file)
    )


@block.limit(_limit)
async def readJson(file: Path | str):
    import json
    return json.loads(
        await readText(file)
    )


async def md5File(file: Path | str):
    return bfunc.md5Bytes(
        await readBytes(file)
    )


async def crcFile(file: Path | str):
    return bfunc.crcBytes(
        await readBytes(file)
    )
