from egopy.event import EventEngine

from egopy.trader.engine import MainEngine
from egopy.trader.ui import MainWindow, create_qapp

#from ego_tts import TtsGateway
from ego_ctp import CtpGateway

from ego_ctastrategy import CtaStrategyApp
from ego_spreadtrading import SpreadTradingApp
from ego_portfoliostrategy import PortfolioStrategyApp


def main():
    """"""
    qapp = create_qapp()

    event_engine = EventEngine()

    main_engine = MainEngine(event_engine)

    #main_engine.add_gateway(TtsGateway)
    main_engine.add_gateway(CtpGateway)

    x = input('Input 1 for Paper & Test, else for TraderApp!\n')
    if x == '1':
        main_engine.add_app(PaperAccountApp)
        main_engine.add_app(CtaBacktesterApp)

    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(PortfolioStrategyApp)
    main_engine.add_app(SpreadTradingApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
