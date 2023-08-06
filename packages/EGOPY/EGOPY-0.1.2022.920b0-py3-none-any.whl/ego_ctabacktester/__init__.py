from pathlib import Path

import importlib_metadata
from egopy.trader.app import BaseApp

from .engine import BacktesterEngine, APP_NAME


try:
    __version__ = importlib_metadata.version("ego_ctabacktester")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"


class CtaBacktesterApp(BaseApp):
    """"""

    app_name: str = APP_NAME
    app_module: str = __module__
    app_path: Path = Path(__file__).parent
    display_name: str = "EGOPY 回测系统"
    engine_class: BacktesterEngine = BacktesterEngine
    widget_name: str = "BacktesterManager"
    icon_name: str = str(app_path.joinpath("ui", "backtester.ico"))
