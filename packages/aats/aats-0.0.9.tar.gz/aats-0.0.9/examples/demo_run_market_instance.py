import time
import sys
sys.path.insert(0,'/home/zhangtian/dev/algo-client-api/src/')
from aats.market_service import MarketService
from aats.market_service import NetWorkType

# maintain your unique cid symbol mapping table which needs to be consistent in both market engine and trade engine
sym_cid_map = {
    1001: "BTCUSDT.BINANCE",
    1002: "ETHUSDT.BINANCE",
    1003: "DOGEUSDT.BINANCE",
    1004: "BTCUSDTSWAP.BINANCE_SWAP"
    }
# control_server_ip = "127.0.0.1"
control_server_ip = "54.199.162.238"
# start market engine
mkt_service = MarketService(sym_cid_map)
mkt_service.set_control_server(ip=control_server_ip, port=8060)  # default setting
mkt_service.set_network_cfg(ip=control_server_ip, port=15002, send_type=NetWorkType.P2P, netcard_name = '')
mkt_service.add_listen_symbol('BTCUSDT', 'BINANCE', 5)
mkt_service.add_listen_symbol('ETHUSDT', 'BINANCE', 5)
# mkt_engine.add_listen_symbol('DOGEUSDT', 'BINANCE', 5)
# mkt_engine.add_listen_symbol('BTCUSDTSWAP', 'BINANCE_SWAP', 5)
mkt_service.run()