
from pathlib import Path
from egopy.trader.app import BaseApp
from .engine import OptionEngine, APP_NAME


class OptionMasterApp(BaseApp):
    """"""
    app_name: str = APP_NAME
    app_module: str = __module__
    app_path: Path = Path(__file__).parent
    display_name: str = "EGOPY 期权交易"
    engine_class: OptionEngine = OptionEngine
    widget_name: str = "OptionManager"
    icon_name: str = str(app_path.joinpath("ui", "option.png"))
