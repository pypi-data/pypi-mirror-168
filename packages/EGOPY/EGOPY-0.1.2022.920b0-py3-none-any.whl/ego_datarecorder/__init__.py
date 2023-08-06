from pathlib import Path

import importlib_metadata
from egopy.trader.app import BaseApp

from .engine import RecorderEngine, APP_NAME


class DataRecorderApp(BaseApp):
    """"""

    app_name: str = APP_NAME
    app_module: str = __module__
    app_path: Path = Path(__file__).parent
    display_name: str = "EGOPY 数据记录(&D)"
    engine_class: RecorderEngine = RecorderEngine
    widget_name: str = "RecorderManager"
    icon_name: str = str(app_path.joinpath("ui", "recorder.png"))
