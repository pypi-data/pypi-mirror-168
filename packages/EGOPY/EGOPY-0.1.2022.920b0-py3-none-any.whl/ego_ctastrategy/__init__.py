from pathlib import Path

import importlib_metadata
from egopy.trader.app import BaseApp
from egopy.trader.constant import Direction
from egopy.trader.object import TickData, BarData, TradeData, OrderData, PositionData
from egopy.trader.utility import BarGenerator, ArrayManager

from .base import APP_NAME, StopOrder
from .engine import CtaEngine
from .template import CtaTemplate, CtaSignal, TargetPosTemplate


class CtaStrategyApp(BaseApp):
    """"""

    app_name: str = APP_NAME
    app_module: str = __module__
    app_path: Path = Path(__file__).parent
    display_name: str = "EGOPY 闪电出击(&F)"
    engine_class: CtaEngine = CtaEngine
    widget_name: str = "CtaManager"
    icon_name: str = str(app_path.joinpath("ui", "cta.png"))
