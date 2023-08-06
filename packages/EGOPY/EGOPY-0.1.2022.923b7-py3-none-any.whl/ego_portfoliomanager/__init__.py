
from pathlib import Path

import importlib_metadata
from egopy.trader.app import BaseApp

from .engine import PortfolioEngine, APP_NAME


class PortfolioManagerApp(BaseApp):
    """"""

    app_name = APP_NAME
    app_module = __module__
    app_path = Path(__file__).parent
    display_name = "EGOPY 业绩监控"
    engine_class = PortfolioEngine
    widget_name = "PortfolioManager"
    icon_name = str(app_path.joinpath("ui", "portfolio.png"))

