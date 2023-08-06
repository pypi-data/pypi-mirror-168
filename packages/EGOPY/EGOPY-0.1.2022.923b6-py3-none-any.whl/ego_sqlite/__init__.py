import importlib_metadata

from .sqlite_database import SqliteDatabase as Database


try:
    __version__ = importlib_metadata.version("ego_sqlite")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"
