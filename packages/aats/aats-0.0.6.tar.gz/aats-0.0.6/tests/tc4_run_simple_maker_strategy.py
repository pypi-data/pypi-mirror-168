
import sys
sys.path.insert(0,'/home/zhangtian/dev/algo-client-api/src/')
import time
from aats.trade_service import TradeService
from aats.base_strategy import BaseStrategy
from aats.base.order import Order
from aats.base.const import OrderType, OrderStatus, Side
from aats.market_service import NetWorkType


sym_cid_map = {
    1001: "BTCUSDT.BINANCE",
    1002: "ETHUSDT.BINANCE",
    1003: "DOGEUSDT.BINANCE"
    }

## define your strategy
class SimpleMakerStrategy(BaseStrategy):
    """
    Naive Maker Strategy: quote on best bid price and ask price
    """
    def __init__(self, *args):
        self.active_orders = {Side.BUY.value: [], Side.SELL.value: []}
        self.pending_orders = {Side.BUY.value: [], Side.SELL.value: []}
        self.cancelling_orders = []

    def close(self):
        for order in self.active_orders:
            self.send_cancel_order(order.order_id)
        
    def onNotify(self, no_type):
        if no_type == 1:
            bid_tgt_px = self.si[self.trade_cid].bid_px * (1-0.0001)
            ask_tgt_px = self.si[self.trade_cid].ask_px * (1+0.0001)
            self.maintain_order(Side.BUY.value, bid_tgt_px)
            self.maintain_order(Side.SELL.value, ask_tgt_px)

    
    def maintain_order(self, side, qpx):
        if len(self.active_orders[side]) >= 1:
            order = self.active_orders[side][0]
            opx = order.price
            if abs(qpx/opx-1) > 0.0001:
                if order.order_id not in self.cancelling_orders:
                    print(f"send cancel order id={order.order_id}")
                    self.cancelling_orders.append(order.order_id)
                    self.send_cancel_order(order.order_id)
        elif len(self.pending_orders[side]) == 0:
            size = 0.001
            order = Order(exchange=self.trade_exchange, 
                            symbol=self.trade_symbol, 
                            price=qpx, 
                            size=size, 
                            side=side, 
                            tif=OrderType.POS.value
                            )
            self.pending_orders[side].append(order)
            print(f"send order id {order.order_id}: px {qpx}, side {side}")
            self.send_order(order)

    
    def onOrderCreated(self, msg):
        order_id = msg.get("order").get("order_id")
        side =  msg.get("order").get("side")
        for order in self.pending_orders[side]:
            if order.order_id == order_id:
                order.order_status = OrderStatus.ADD
                self.active_orders[side].append(order)
                self.pending_orders[side].remove(order)
                return

        
    def onOrderAcked(self, msg):
        order_id = msg.get("order").get("order_id")
        side =  msg.get("order").get("side")
        for order in self.active_orders[side]:
            if order.order_id == order_id:
                order.order_status = OrderStatus.ACK
                return

    def onOrderRejected(self, msg):
        order_id = msg.get("order").get("order_id")
        side =  msg.get("order").get("side")
        for order in self.active_orders[side]:
            if order.order_id == order_id:
                order.order_status = OrderStatus.RJD
                self.pending_orders[side].remove(order)
                return

    def onOrderCancelCreated(self, msg):
        order_id = msg.get("order").get("order_id")
        side =  msg.get("order").get("side")
        for order in self.active_orders[side]:
            if order.order_id == order_id:
                order.order_status = OrderStatus.CXL
                self.cancelling_orders.remove(order_id)
                return

    def onOrderCancelAcked(self, msg):
        order_id = msg.get("order").get("order_id")
        side =  msg.get("order").get("side")
        for order in self.active_orders[side]:
            if order.order_id == order_id:
                order.order_status = OrderStatus.CAK
                return

    def onOrderCancelRejected(self, msg):
        order_id = msg.get("order").get("order_id")
        side =  msg.get("order").get("side")
        for order in self.active_orders[side]:
            if order.order_id == order_id:
                order.order_status = OrderStatus.CRD
                self.active_orders[side].remove(order)
                return

    def onOrderExec(self, msg):
        order_id = msg.get("order").get("order_id")
        fill_size = float(msg.get("order").get("fill_size"))
        side =  msg.get("order").get("side")
        for order in self.active_orders[side]:
            if order.order_id == order_id:
                order.fill_size += fill_size
                if abs(order.fill_size-order.size) < 1e-8:
                    order.order_status = OrderStatus.EXE
                    self.active_orders[side].remove(order)
                    return

    def onOrderCanceled(self, msg):
        order_id = msg.get("order").get("order_id")
        side =  msg.get("order").get("side")
        for order in self.active_orders[side]:
            if order.order_id == order_id:
                order.order_status = OrderStatus.CXD
                self.active_orders[side].remove(order)
                return

    def onOrderClosed(self, msg):
        order_id = msg.get("order").get("order_id")
        side =  msg.get("order").get("side")
        for order in self.active_orders[side]:
            if order.order_id == order_id:
                order.order_status = OrderStatus.CLD
                self.active_orders[side].remove(order)
                return




# init trade engine
trade_service = TradeService(sym_cid_map)

# setup public config
trade_service.set_md_connection(ip='127.0.0.1', port=15006, send_type = NetWorkType.P2P)  # for P2P mode, port is required to use the port from market server
trade_service.add_md_symbol(symbol='BTCUSDT', exchange='BINANCE', level_num=5)
# trade_service.add_md_symbol(symbol='DOGEUSDT', exchange='BINANCE')

# setup private config
trade_service.set_ts_connection(ip='localhost', port=8060)  # default setting
trade_service.config_exchange(exchange='BINANCE', trade_type='sandbox')
trade_service.set_apikey(exchange="BINANCE", 
                        key="02SvhZEYG1p92JWdekP75XQKayqfLxmjHWNEfWU1KrCPjJ5xrLcOU1YHZ5SUBVFA", 
                        secret="iKnZvDKMGQuEINhjDX8gbIVJDLl48fV6GFLL5gcFT8Sfj9yxGrnP7uFm7AAVWeFP", 
                        password="",
                        subaccount="")
trade_service.set_fee('BINANCE', 0.0003, 0)
trade_service.add_trade_symbol(symbol='BTCUSDT', exchange='BINANCE', level_num=5)

# setup your strategy
my_strategy = SimpleMakerStrategy()
trade_service.add_strategy(my_strategy)

# start run
try:
    trade_service.run()
except KeyboardInterrupt as err:
    # trade_service.stop()
    print("close strategy and close open orders")
    # trade_service.manager.stop()
    my_strategy.close()
    time.sleep(1)
    print("trade closed")    