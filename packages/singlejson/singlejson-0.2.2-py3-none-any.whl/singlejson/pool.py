"""The main files handling the file pool."""
from typing import Dict, Any
from .fileutils import JSONFile, abs_filename

_file_pool: Dict[str, JSONFile] = {}


def load(filename: str, default: Any = "{}") -> JSONFile:
    """
    Open a JsonFile (synchronously)
    :param filename: Path to JSON file on disk
    :param default: Default file contents to save if file is nonexistent
    :return: the corresponding JsonFile
    """
    filename = abs_filename(filename)
    if filename not in _file_pool:
        _file_pool[filename] = JSONFile(filename, default=default)
    return _file_pool[filename]


def sync():
    """
    Sync changes to the filesystem
    :return:
    """
    for file in _file_pool.values():
        file.save()
