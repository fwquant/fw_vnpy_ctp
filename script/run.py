from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from fw_vnpy_ctp import CtpGateway as fw_CtpGateway
# from vnpy_ctp import CtpGateway

def main():
    """主入口函数"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    # main_engine.add_gateway(gateway_class=CtpGateway, gateway_name="CTP")
    # main_engine.add_gateway(gateway_class=CtpGateway, gateway_name="CTP-yinhe-163")
    # main_engine.add_gateway(gateway_class=CtpGateway, gateway_name="CTP-simnow")
    main_engine.add_gateway(gateway_class=fw_CtpGateway, gateway_name="CTP-yinhe-fw")
    main_engine.add_gateway(gateway_class=fw_CtpGateway, gateway_name="CTP-simnow-fw")

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
