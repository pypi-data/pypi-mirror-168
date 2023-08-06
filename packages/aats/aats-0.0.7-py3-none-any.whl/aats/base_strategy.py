from aats.base.manager import Manager
from aats.base.utils import timeit
from aats.base.order import Order

class BaseStrategy(object):
    def __init__(self, *args):
        pass
    
    def init_strategy(self, si, trade_cid, trade_symbol, trade_exchange):
        self.si = si
        self.manager = Manager()
        self.tick_cnt = 0
        self.quote_cnt = 0
        self.trade_cid = trade_cid
        self.trade_symbol = trade_symbol
        self.trade_exchange = trade_exchange
        self.level_num = self.si[self.trade_cid].level_num
        self.bid_px_names = [f'bid_{i}_px' for i in range(self.level_num)]
        self.bid_qty_names = [f'bid_{i}_qty' for i in range(self.level_num)]
        self.ask_px_names = [f'ask_{i}_px' for i in range(self.level_num)]
        self.ask_qty_names = [f'ask_{i}_qty' for i in range(self.level_num)]

    # @timeit
    def onQuote(self, msg):
        cid = msg.get("cid")
        if cid not in self.si.keys():
            return
        self.si[cid].bid_px = msg.get("bid_0_px")
        self.si[cid].bid_qty = msg.get("bid_0_qty")
        self.si[cid].ask_px = msg.get("ask_0_px")
        self.si[cid].ask_qty = msg.get("ask_0_qty")
        self.si[cid].mid_px = (self.si[cid].bid_px + self.si[cid].ask_px) / 2
        self.si[cid].bids = [[msg[self.bid_px_names[i]],msg[self.bid_qty_names[i]]] for i in range(self.level_num)]
        self.si[cid].asks = [[msg[self.ask_px_names[i]],msg[self.ask_qty_names[i]]] for i in range(self.level_num)]
        # print(f"BaseStrategy onQuote: bidpx {self.si[cid].bid_px}, askxp {self.si[cid].ask_px}")
        self.onNotify(1)

    # @timeit
    def onTick(self, msg):
        cid = msg.get("cid")
        if cid not in self.si.keys():
            return
        self.si[cid].trade_px = msg.get("px")
        self.si[cid].trade_qty = msg.get("qty")
        self.si[cid].trade_type = msg.get("tradeType")
        # print(f"BaseStrategy onTick: tradepx {self.si[cid].trade_px}, trade_qty {self.si[cid].trade_qty}, trade_type {self.si[cid].trade_type}")
        self.onNotify(0)

    def close(self):
        pass
    
    def onNotify(self, no_type):
        pass
        # raise NotImplementedError("BaseStrategy onNotify has not been implemented yet")

    def send_order(self, order):
        self.manager.place_order(order)
        
    def send_cancel_order(self, order_id):
        self.manager.cancel_order(order_id)

    def onOrderCreated(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderCreated has not been implemented yet")

    def onOrderAcked(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderAcked has not been implemented yet")

    def onOrderRejected(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderRejected has not been implemented yet")

    def onOrderCancelCreated(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderCancelCreated has not been implemented yet")

    def onOrderCancelAcked(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderCancelAcked has not been implemented yet")

    def onOrderCancelRejected(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderCancelRejected has not been implemented yet")

    def onOrderExec(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderExec has not been implemented yet")

    def onOrderCanceled(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderCanceled has not been implemented yet")

    def onOrderClosed(self, msg):
        pass
        # raise NotImplementedError("BaseStrategy onOrderClosed has not been implemented yet")
