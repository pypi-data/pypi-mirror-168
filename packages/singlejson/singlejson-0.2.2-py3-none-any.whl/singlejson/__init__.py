"""
A package for easily maintaining JSON files

open a JSON file using open()
if you call open with the same filename again, the same object will be returned.
sync all changes to disk using sync()
"""
from .fileutils import JSONFile
from .pool import load, sync

__all__ = ["JSONFile", "load", "sync"]

VERSION: str = "0.2.2"
