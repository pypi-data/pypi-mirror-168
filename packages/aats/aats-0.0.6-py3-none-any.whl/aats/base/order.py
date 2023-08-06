from dataclasses import dataclass, field
from itertools import count
from enum import Enum
from aats.base.const import OrderStatus

@dataclass
class Order:
    """
    Order object
    Mandatory field: exchange, symbol, price, size, side, tif (order type, currently support IOC and Post Only)
    """
    exchange: str
    symbol: str
    price: float
    size: float
    side: str
    tif: str
    order_id: int = field(default_factory=count(start=1).__next__, init=False)
    margin: bool = False
    margin_source: str = 'spot'
    fill_size: float = 0 
    fill_price: float = 0
    fill_notional: float = 0
    remote_id: int = 0
    order_status: Enum = OrderStatus.NEW



if __name__ == "__main__":
    # new_order = Order(exchange='BINANCE', symbol='BTCUSDT', price=100, size=0.01, side='buy', tif='pos')
    for i in range(10):
        new_order = Order(exchange='BINANCE', symbol='BTCUSDT', price=100, size=0.01, side='buy', tif='pos')
        print(new_order)