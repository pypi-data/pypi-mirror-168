from aats.base.utils import *
from dataclasses import dataclass

class SymbolInfo(object):
    def __init__(self, cid, sym, exch, level_num):
        self.cid = cid
        self.sym = sym
        self.exch = exch
        self.level_num = level_num
        self.port = self.sym+'.'+self.exch
        self.trade_px = 0.0
        self.trade_qty = 0.0
        self.bid_px = 0.0
        self.ask_px = 0.0
        self.bid_qty = 0.0
        self.ask_qty = 0.0
        self.asks = []
        self.bids = []
        self.ticksize = 0.0
        
        

