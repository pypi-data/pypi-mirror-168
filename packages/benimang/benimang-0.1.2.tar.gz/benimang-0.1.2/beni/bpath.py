import os
import shutil
from pathlib import Path

def get(path: str | Path, expand: str = ''):
    if type(path) is not Path:
        path = Path(path)
    return path.joinpath(expand).resolve()


def getUser(expand: str = ''):
    return get(Path('~').expanduser(), expand)


def getWorkspace(expand: str = ''):
    return getUser(f'beni.workspace/{expand}')


def getDesktop(expand: str = ''):
    return getUser(f'Desktop/{expand}')


def openDir(dir: Path | str):
    os.system(f'start explorer {dir}')


def remove(path: Path | str):
    if type(path) is not Path:
        path = get(path)
    if path.is_file():
        path.unlink(True)
    elif path.is_dir():
        shutil.rmtree(path)


def make(path: Path | str):
    if type(path) is not Path:
        path = get(path)
    path.mkdir(parents=True, exist_ok=True)


def clearDir(dir: Path):
    for sub in dir.iterdir():
        remove(sub)


def copy(src: Path | str, dst: Path | str):
    if type(src) is not Path:
        src = get(src)
    if type(dst) is not Path:
        dst = get(dst)
    make(dst.parent)
    if src.is_file():
        shutil.copyfile(src, dst)
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        if not src.exists():
            raise Exception(f'copy error: src not exists {src}')
        else:
            raise Exception(f'copy error: src not support {src}')


def move(src: Path | str, dst: Path | str, force: bool = False):
    if type(src) is not Path:
        src = get(src)
    if type(dst) is not Path:
        dst = get(dst)
    if dst.exists():
        if force:
            remove(dst)
        else:
            raise Exception(f'move error: dst exists {dst}')
    make(dst.parent)
    os.rename(src, dst)


def renameName(src: Path | str, name: str):
    if type(src) is not Path:
        src = get(src)
    src.rename(src.with_name(name))


def renameStem(src: Path | str, stemName: str):
    if type(src) is not Path:
        src = get(src)
    src.rename(src.with_stem(stemName))


def renameSuffix(src: Path | str, suffixName: str):
    if type(src) is not Path:
        src = get(src)
    src.rename(src.with_suffix(suffixName))


def listPath(path: Path | str, recursive: bool = False):
    '''获取指定路径下文件以及目录列表'''
    if type(path) is not Path:
        path = get(path)
    if recursive:
        return list(path.glob('**/*'))
    else:
        return list(path.glob("*"))


def listFile(path: Path | str, recursive: bool = False):
    '''获取指定路径下文件列表'''
    if type(path) is not Path:
        path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_file(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_file(), path.glob('*')))


def listDir(path: Path | str, recursive: bool = False):
    '''获取指定路径下目录列表'''
    if type(path) is not Path:
        path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_dir(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_dir(), path.glob('*')))

