from pathlib import Path

from egopy.trader.app import BaseApp

from .engine import ChartWizardEngine, APP_NAME


class ChartWizardApp(BaseApp):
    """"""
    
    app_name: str = APP_NAME
    app_module: str = __module__
    app_path: Path = Path(__file__).parent
    display_name: str = "EGOPY 实时K线"
    engine_class: ChartWizardEngine = ChartWizardEngine
    widget_name: str = "ChartWizardWidget"
    icon_name: str = str(app_path.joinpath("ui", "cw.png"))
