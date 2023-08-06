import socket
import json
from enum import Enum 
from struct import pack, unpack

class ControlService(object):
    def __init__(self):
        return

    def set_control_server(self, ip, port):
        self.control_ip = ip
        self.control_port = port

    def show_all_trade_servers(self):
        s = socket.socket()
        s.connect((self.control_ip, self.control_port))
        msg = json.dumps({"type": "show_all_trade_instance"})
        self.send_msg(msg, s)
        data = s.recv(1024)
        length = unpack('i', data[:4])[0]
        resp = json.loads(data[4:length+4].decode('utf-8'))
        data = resp.get("data").get("result").split("\n")
        server_list = [{"pid": item.split()[0], "port": item.split()[2]} for item in data if item]
        print("active trade server list: ", server_list)

    def show_all_market_servers(self):
        s = socket.socket()
        s.connect((self.control_ip, self.control_port))
        msg = json.dumps({"type": "show_all_market_instance"})
        self.send_msg(msg, s)
        data = s.recv(1024)
        length = unpack('i', data[:4])[0]
        resp = json.loads(data[4:length+4].decode('utf-8'))
        data = resp.get("data").get("result").split("\n")
        server_list = [{"pid": item.split()[0], "port": item.split()[3]} for item in data if item]
        print("active market server list: ", server_list)

    def kill_server(self, pid):
        s = socket.socket()
        s.connect((self.control_ip, self.control_port))
        msg = json.dumps({"type": "kill_process", "pid":pid})
        self.send_msg(msg, s)
        data = s.recv(1024)
        length = unpack('i', data[:4])[0]
        resp = json.loads(data[4:length+4].decode('utf-8'))
        print(resp)

    def send_msg(self, msg, socket):
        message_len = len(msg)
        message_format = '>i' + str(message_len) + 's'
        send_message = pack(message_format, message_len,msg.encode('utf-8'))
        socket.send(send_message)

        

