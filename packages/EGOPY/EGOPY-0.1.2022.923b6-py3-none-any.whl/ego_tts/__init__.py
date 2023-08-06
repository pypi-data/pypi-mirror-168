import importlib_metadata

from .gateway import TtsGateway


try:
    __version__ = importlib_metadata.version("ego_tts")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"
