from aats.base_strategy import BaseStrategy
from aats.base.order import Order
from aats.base.const import OrderType, OrderStatus, Side
import time

class SimpleTakerStrategy(BaseStrategy):
    """
    Naive Taker Strategy: place IOC buy order on fixed time interval
    """
    def __init__(self, msecs):
        self.msecs = msecs
        self.start_time = time.time_ns()
        self.next_fire_time = self.start_time + self.msecs * 1e6

    def onNotify(self, No_type):
        current_time = time.time_ns()
        if current_time > self.next_fire_time:
            self.next_fire_time = current_time + self.msecs * 1e6
            self.onTimer()

    def onTimer(self):
        qpx = self.si[self.trade_cid].ask_px
        size = 0.001
        new_order = Order(exchange=self.trade_exchange, 
                            symbol=self.trade_symbol, 
                            price=qpx, 
                            size=size, 
                            side=Side.BUY.value, 
                            tif=OrderType.IOC.value)
        self.send_order(new_order)
        print(f"send order {new_order}")

