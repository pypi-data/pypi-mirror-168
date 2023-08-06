import os
import os.path
from enum import Enum
from glob import glob


def last_modefied_file_in(dir: os.path, ext: str):
    files = file_list_in(dir, ext, FileSortType.UpdateTime, reverse_order=True)
    if files.__len__() > 0:
        return files[0]

    return ''


class FileSortType(Enum):
    Name = 1
    UpdateTime = 2


def file_list_in(dir: os.path, ext: str, sort_type: FileSortType = FileSortType.Name, reverse_order: bool = False):
    files = glob(dir + f'/**/*.{ext}', recursive=True)

    if sort_type == FileSortType.Name:
        return sorted(files, key=os.path.basename, reverse=reverse_order)
    if sort_type == FileSortType.UpdateTime:
        return sorted(files, key=os.path.getmtime, reverse=reverse_order)

    raise RuntimeError('invalid file sort type')
