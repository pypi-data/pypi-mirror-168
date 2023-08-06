from typing import Any, Final

from beni import bfile, bpath


async def get(key: str, default: Any = None):
    storageFile = _getStorageFile(key)
    if storageFile.is_file():
        return await bfile.readYaml(storageFile)
    else:
        return default


async def set(key: str, value: Any):
    storageFile = _getStorageFile(key)
    await bfile.writeYaml(storageFile, value)


async def clear(*keyList: str):
    for key in keyList:
        storageFile = _getStorageFile(key)
        bpath.remove(storageFile)


async def clearAll():
    for storageFile in bpath.listFile(_storagePath):
        bpath.remove(storageFile)

# ------------------------------------------------------------------------------------------

_storagePath: Final = bpath.getWorkspace('.storage')


def _getStorageFile(key: str):
    return bpath.get(_storagePath, f'{key}.yaml')
