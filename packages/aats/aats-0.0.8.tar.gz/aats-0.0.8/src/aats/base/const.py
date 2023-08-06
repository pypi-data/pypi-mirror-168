from enum import Enum

class OrderType(Enum):
    """Order Type"""
    IOC = "ioc"   # immediate filled or cancel
    POS = "pos"   # post only for market making


class OrderStatus(Enum):
    """Order status"""
    NEW = "NEW"   # new order (default)
    ADD = "ADD"   # create order
    CXL = "CXL"   # cancel order 
    ACK = "ACK"   # order create acknowledged 
    CAK = "CAK"   # order cancel acknowledged 
    EXE = "EXE"   # order executed 
    RJD = "RJD"   # order rejected 
    CRD = "CRD"   # order cancel rejected 
    CXD = "CXD"   # order cancelled and closed
    CLD = "CLD"   # order closed
    UNK = "UNK"   # order unknown 

class Side(Enum):
    """Side of order/trade"""
    BUY = "buy"
    SELL = "sell"
