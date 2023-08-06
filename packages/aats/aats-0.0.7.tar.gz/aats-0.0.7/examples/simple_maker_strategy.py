from aats.base_strategy import BaseStrategy
from aats.base.order import Order
from aats.base.const import OrderType, OrderStatus, Side

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