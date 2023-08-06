import time
import datetime
from queue import Queue, Empty
from threading import *
import socket
from struct import pack, unpack
import threading
import json
from collections import namedtuple
from aats.base.singleton import singleton
import signal


tick = namedtuple('tick', 'type cid tradeType qty px')
book5 = namedtuple('book5', 'type cid length bid_0_qty bid_0_px bid_1_qty bid_1_px bid_2_qty bid_2_px bid_3_qty bid_3_px bid_4_qty bid_4_px ask_0_qty ask_0_px ask_1_qty ask_1_px ask_2_qty ask_2_px ask_3_qty ask_3_px ask_4_qty ask_4_px')

@singleton
class Manager(object):
    def __init__(self):
        self.__event_queue = Queue()
        self.__md_queue = Queue()
        self._current_md_message = bytes()
        self._current_md_last_len = 0
        self.__active = False
        self.__thread = Thread(target=self.__run)
        self.count = 0
        self.__handlers = {}

    def init_manager(self, cfg):
        self.cfg = cfg
        self.HOST = cfg['server_ip']
        self.SERVER_PORT = cfg['server_port']
        self.SEND_TO_IP = cfg['send_to_ip']
        self.SEND_TO_PORT = cfg['send_to_port']
        self.md_send_type = cfg['md_send_type']
        self.INSTANCE_PORT = None
        self.trade_cfg = {'exchanges': cfg['exchanges'], 'apikeys': cfg['apikeys'], 'symbol_info': cfg['symbol_info'], 'symbols': cfg['trade_symbols'], 'fees': cfg['fees']}
    
    def __run(self):
        while self.__active == True:
            try:
                # if self.__event_queue.qsize() >= 2:
                #     print("event size in queue: ", self.__event_queue.qsize())
                event = self.__event_queue.get(block=True, timeout=1)
                self.__event_process(event)
            except Empty:
                pass
            self.count += 1
    
    def __event_process(self, event):
        if event.get('type') in self.__handlers:
            for handler in self.__handlers[event.get('type')]:
                handler(event)
        self.count += 1
    
    def start(self):
        self.__active = True
        self.__thread.start()
        self.count += 1
        self.socket_connect()
        signal.pause()

    def stop(self):
        self.__active = False
        self.__thread.join()
        self.count += 1

    def add_event_listener(self, type_, handler):
        print(f"{datetime.datetime.now()} {self.count}_add_event_listener: {type_} {handler.__name__}")
        try:
            handler_list = self.__handlers[type_]
        except KeyError:
            handler_list = []
        self.__handlers[type_] = handler_list
        if handler not in handler_list:
            handler_list.append(handler)
        self.count += 1

    def remove_event_listener(self, type_, handler):
        try:
            handler_list = self.handlers[type_]
            if handler in handler_list:
                handler_list.remove(handler)
            if not handler_list:
                del self.handlers[type_]
        except KeyError:
            pass
        self.count += 1

    def send_event(self, event):
        self.__event_queue.put(event)
        self.count += 1

    def subscrib_strategy(self, strategy):
        self.add_event_listener('onQuote', strategy.onQuote)
        self.add_event_listener('onTick', strategy.onTick)
        self.add_event_listener('onNotify', strategy.onNotify)

        self.add_event_listener('onOrderCreated', strategy.onOrderCreated)
        self.add_event_listener('onOrderAcked', strategy.onOrderAcked)
        self.add_event_listener('onOrderCancelCreated', strategy.onOrderCancelCreated)
        self.add_event_listener('onOrderCancelAcked', strategy.onOrderCancelAcked)
        self.add_event_listener('onOrderCancelRejected', strategy.onOrderCancelRejected)
        self.add_event_listener('onOrderCanceled', strategy.onOrderCanceled)
        self.add_event_listener('onOrderExec', strategy.onOrderExec)
        self.add_event_listener('onOrderRejected', strategy.onOrderRejected)
        self.add_event_listener('onOrderClosed', strategy.onOrderClosed)
 
    def socket_connect(self):
        # connect server socket
        self.server_socket = socket.socket()
        self.server_socket.connect((self.HOST, self.SERVER_PORT))
        # request new instance and wait for pin and instance port
        msg = {'type': 'new_trade_instance'}
        msg = json.dumps(msg)
        self.send_msg(msg, self.server_socket)
        data = self.server_socket.recv(1024)
        # print(data)
        length = unpack('i', data[:4])[0]
        resp = json.loads(data[4:length+4].decode('utf-8'))
        self.PIN = resp.get("data").get("pin")
        self.INSTANCE_PORT = int(resp.get("data").get("port"))
        print(f"PIN: {self.PIN}, PORT: {self.INSTANCE_PORT}")
        # close server socket and connect instance socket
        self.server_socket.close()
        time.sleep(1)
        self.instance_socket = socket.socket()
        self.instance_socket.connect((self.HOST, int(self.INSTANCE_PORT)))
        self.trade_thread = threading.Thread(target=self.recv_msg)
        self.market_thread = threading.Thread(target=self.subscribe_market_data)
        self.market_data_process_thread = threading.Thread(target=self.get_md_data)
        self.trade_thread.start()
        self.market_thread.start()
        self.login()
        self.load_config()
    


    def login(self):
        msg = {'type': 'login','data': {'pin': self.PIN}}
        msg = json.dumps(msg)
        # print("send login msg: ", msg)
        self.send_msg(msg, self.instance_socket)

    def load_config(self):
        msg = {"type": "init", "data": self.trade_cfg}
        print("load config: ", msg)
        msg = json.dumps(msg)
        self.send_msg(msg, self.instance_socket)


    def place_order(self, order):
        msg = {
                "type": "place_order",
                    "data": {
                        "exchange": str(order.exchange),
                        "symbol": str(order.symbol),
                        "order_id": str(order.order_id),
                        "price": str(order.price),
                        "size": str(order.size),
                        "side": str(order.side),
                        "tif": str(order.tif),
                        "margin": order.margin,
                        "margin_source": str(order.margin_source)
                    }   
                }
        msg = json.dumps(msg)
        self.send_msg(msg, self.instance_socket)

    def cancel_order(self, order_id):
        msg = {
                "type": "cancel_order",
                    "data": 
                    {
                        "order_id": order_id
                    }   
                }
        msg = json.dumps(msg)
        self.send_msg(msg, self.instance_socket)

    def send_msg(self, msg, socket):
        message_len = len(msg)
        message_format = '>i' + str(message_len) + 's'
        send_message = pack(message_format, message_len,msg.encode('utf-8'))
        socket.send(send_message)
        # print(send_message)
    def ping(self,resp):
        ts = resp.get("ts")
        msg = {"type": "pong", "ts": ts}        
        msg = json.dumps(msg)
        # print(msg)
        self.send_msg(msg, self.instance_socket)

    def recv_msg(self):
        # print(f"PID = {os.getpid()}, TID = {threading.get_ident()}")
        while True:
            try:                        
                data = self.instance_socket.recv(4)
                msg_length = int.from_bytes(data, "little")
                if msg_length <= 0:
                    return
                # print("trade recv msg len: "+ str(msg_length))
                buf = self.instance_socket.recv(msg_length)

                data = buf
                buf_len = len(buf)

                while buf_len < msg_length:                
                    buf = self.instance_socket.recv(msg_length - buf_len)
                    data = data + buf
                    buf_len = buf_len + len(buf)

                # print(data)
                # length = unpack('i', data[:4])[0]
                response = data[:msg_length].decode('utf-8')
                curr_time = time.time_ns()
                print(f"{curr_time}ns recv msg: {response}")
                resp = json.loads(response)
                if resp.get("type") == 'init':
                    if resp.get("result") == 'ok':
                        print("load config success")
                        self.send_event(resp)
                    else:
                        print("load config failed")
                elif resp.get("type") == 'ping':
                    self.ping(resp)
                elif resp.get("type") in ["login", "place_order", "cancel_order", "onOrderCreated", "onOrderAcked", "onOrderCancelCreated", "onOrderCancelAcked", 
                                            "onOrderCancelRejected", "onOrderCanceled", "onOrderExec", "onOrderRejected", "onOrderClosed"]:
                    self.send_event(resp)
                else:
                    print(f"type {resp.get('type')} is out of scope")
            except Exception as err:
                print(f"recv msg error with raw data {data}")
                raise err
    
    def process_md_data(self):
        # print(self._current_md_message)
        msg  = self._current_md_message
        messageType = unpack("=c", msg[:1])
        iType = int.from_bytes(messageType[0], 'little')
        
        if iType == 0:  # tick
            t = tick._make(unpack("=ciidd", msg[:25]))
            msg = t._asdict()
            msg['type'] = 'onTick'
            self.send_event(msg)
        elif iType == 1:  # level 5
            depth = unpack('i',msg[5:9])[0]
            b = book5._make(unpack("=cii"+"dddd"*depth,msg))
            msg = b._asdict()
            msg['type'] = 'onQuote'
            self.send_event(msg)

        self._current_md_message = bytes()
        self._current_md_last_len = 0

    def split_md_data(self,data):
        read_pos = 0
        data_length = len(data)

        # print("read pos: "+ str(read_pos) + " data length: " + str(data_length) + " current data last size: "+ str(self._current_md_last_len))
        while read_pos < data_length:
            if self._current_md_last_len > 0:
                if data_length >= self._current_md_last_len:
                    # print("data_length is: " + str(data_length) + " last size: " + str(self._current_md_last_len))
                    self._current_md_message += data[read_pos:read_pos + self._current_md_last_len]
                    read_pos += self._current_md_last_len
                    self.process_md_data()
                    # print("3. read pos: "+str(read_pos))
                else:
                    self._current_md_message += data[read_pos:data_length]
                    read_pos += data_length - read_pos
                    self._current_md_last_len -= ( data_length - read_pos)
                    # print("4. read pos: "+str(read_pos))
            else:
                self._current_md_last_len = int.from_bytes(data[read_pos:read_pos + 4], "little")
                # print("current last size: " + str(self._current_md_last_len))
                if self._current_md_last_len <= 0:
                    return

                read_pos += 4              
                
                if (data_length - read_pos) >= self._current_md_last_len:
                    self._current_md_message += data[read_pos:read_pos + self._current_md_last_len]
                    read_pos += self._current_md_last_len
                    self.process_md_data()
                    # print("1. read pos: "+str(read_pos))
                else:    
                    self._current_md_message += data[read_pos:data_length]
                    self._current_md_last_len -= ( data_length - read_pos)
                    read_pos += data_length - read_pos
                    # print("2. read pos: "+str(read_pos) + " current last size: " + str(self._current_md_last_len))


    def get_md_data(self):
        while self.__active == True:
            try:
                data = self.__md_queue.get(block=True, timeout=1)
                self.split_md_data(data)
            except Empty:
                pass                

    def md_recv_tcp(self):
        self.timer = 0
        while True:
            data = self.md_sock.recv(10240)
            # print("md recv size: " + str(len(data)) + " md queue size: " + str(self.__md_queue.qsize()))            
            self.__md_queue.put(data)
                             

    def md_recv_udp(self):
        while True:
            msg = self.md_sock.recv(10240)
            # print(len(msg))
            # tick = namedtuple('tick', ['type', 'cid', 'tradeType', 'qty', 'px'])
            messageType = unpack("=c",msg[:1])
            iType = int.from_bytes(messageType[0],'little')
            # print(iType)
            if iType == 0: # tick
                t = tick._make(unpack("=ciidd",msg[:25]))
                msg = t._asdict()
                msg['type'] = 'onTick'
                # msg = {'type': 'onTick', 'cid': t.cid, 'tradeType': 1, 'qty': t.qty, 'px': t.px}
                self.send_event(msg)
            elif iType == 1: # level 5
                depth = unpack('i',msg[5:9])[0]
                b = book5._make(unpack("=cii"+"dddd"*depth,msg))
                msg = b._asdict()
                msg['type'] = 'onQuote'
                self.send_event(msg)

    def subscribe_market_data(self):
        if self.md_send_type == 1:
            IS_ALL_GROUPS = False
            # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            # sock.bind((self.SEND_TO_IP, self.SEND_TO_PORT))
            self.md_sock = socket.socket()
            print("sent type is P2P, connect md server "+self.SEND_TO_IP + " : " + str(self.SEND_TO_PORT))
            self.md_sock.connect((self.SEND_TO_IP, self.SEND_TO_PORT))  # connect to the server
            self.market_data_process_thread.start()
            self.md_recv_tcp()
            
        elif self.md_send_type ==2:
            IS_ALL_GROUPS = False
            md_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            md_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            md_sock.bind((self.SEND_TO_IP, self.SEND_TO_PORT))
            self.md_recv_udp()
        elif self.md_send_type == 3:
            IS_ALL_GROUPS = False
            md_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            md_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            md_sock.bind(('', self.SEND_TO_PORT))
            self.md_recv_udp()
            
        # mreq = pack("4sl", socket.inet_aton(self.SEND_TO_IP), socket.INADDR_ANY)
        # sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    
        



