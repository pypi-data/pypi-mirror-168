import time
from struct import pack, unpack

from aats.base.manager import Manager
from aats.base.symbolinfo import SymbolInfo


class TradeService(object):
    def __init__(self, sym_cid_map):
        start = time.time_ns()
        self.sym_cid_map = sym_cid_map
        self.cid_sym_map = {v: k for k, v in self.sym_cid_map.items()}
        self.si = dict()
        self.cfg = dict()
        self.cfg['exchanges'] = []
        self.cfg['apikeys'] = dict()
        self.cfg['fees'] = dict()
        self.cfg['symbol_info'] = dict()
        self.cfg['md_symbols'] = []
        self.cfg['trade_symbols'] = []

    def set_ts_connection(self, ip, port):
        self.cfg['server_ip'] = ip
        self.cfg['server_port'] = port

    def set_md_connection(self, ip, port, send_type):
        self.cfg['send_to_ip'] = ip
        self.cfg['send_to_port'] = port
        self.cfg['md_send_type'] = send_type.value

    def config_exchange(self, exchange, trade_type):
        self.exchange = exchange
        self.trade_type = trade_type
        self.cfg['exchanges'].append(
            {'exchange': self.exchange, 'trader_type': self.trade_type})

    def set_apikey(self, exchange, key, secret, password, subaccount):
        self.exchange = exchange
        self.key = key
        self.secret = secret
        self.password = password
        self.subaccount = subaccount
        self.cfg['apikeys'][exchange] = {
            'key': self.key, 'secret': self.secret, 'pass': self.password, 'subaccount': self.subaccount}

    def set_fee(self, exchange, taker_fee, maker_fee):
        self.taker_fee = taker_fee
        self.maker_fee = maker_fee
        self.cfg['fees'][exchange] = {
            "take": self.taker_fee, "make": self.maker_fee}

    def add_md_symbol(self, symbol, exchange, level_num=5):
        cid = self.cid_sym_map[symbol+'.'+exchange]
        self.cfg['md_symbols'].append({'cid': cid, 'port': [symbol, exchange]})
        self.si[cid] = SymbolInfo(cid, symbol, exchange, level_num)

    def add_trade_symbol(self, symbol, exchange, level_num=5):
        self.trade_symbol = symbol
        self.trade_exchange = exchange
        self.trade_cid = self.cid_sym_map[symbol+'.'+exchange]
        self.cfg['trade_symbols'].append(
            {'cid': self.trade_cid, 'port': [symbol, exchange]})
        self.si[self.trade_cid] = SymbolInfo(
            self.trade_cid, symbol, exchange, level_num)
        # self.si[cid].trade_flag = True

    def add_strategy(self, strategy):
        self.strategy = strategy

    def run(self):
        self.manager = Manager()
        self.manager.subscrib_strategy(self.strategy)

        self.manager.init_manager(self.cfg)
        self.strategy.init_strategy(
            self.si, self.trade_cid, self.trade_symbol, self.trade_exchange)
        self.manager.start()
        # self.manager.show_all_trade_instances()

