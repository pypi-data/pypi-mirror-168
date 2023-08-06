import sys
sys.path.insert(0,'/home/zhangtian/dev/algo-client-api/src/')
from aats.control_service import ControlService

cs = ControlService()
cs.set_control_server(ip='127.0.0.1', port=8060)

cs.show_all_market_servers()

# cs.show_all_trade_servers()

# cs.kill_server(pid=2535718)