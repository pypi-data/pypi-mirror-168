
from pathlib import Path

from egopy.trader.app import BaseApp
from egopy.trader.constant import Direction
from egopy.trader.object import TickData, BarData, TradeData, OrderData
from egopy.trader.utility import BarGenerator, ArrayManager

from .base import APP_NAME
from .engine import StrategyEngine
from .template import StrategyTemplate
from .backtesting import BacktestingEngine


class PortfolioStrategyApp(BaseApp):
    """"""

    app_name = APP_NAME
    app_module = __module__
    app_path = Path(__file__).parent
    display_name = "EGOPY 联合作战(&C)"
    engine_class = StrategyEngine
    widget_name = "PortfolioStrategyManager"
    icon_name = str(app_path.joinpath("ui", "strategy.png"))
