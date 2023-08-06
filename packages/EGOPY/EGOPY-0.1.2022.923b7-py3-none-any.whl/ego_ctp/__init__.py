import importlib_metadata

from .gateway import CtpGateway


try:
    __version__ = importlib_metadata.version("ego_ctp")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"
