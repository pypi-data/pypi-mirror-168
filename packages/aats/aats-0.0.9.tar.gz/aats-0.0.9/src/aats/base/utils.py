import json
import getpass
import time
from functools import wraps


# def create_symbol_info_cfg(symbols):
#         si = dict()
#         for sym in symbols:
#             fp = f'/data/cc/prod/symbol_info/{sym.split(".")[1]}/{sym.split(".")[0]}.json'
#             scfg = json.load(open(fp))
#             si[sym] = scfg['data'][-1][1]
#         return si

# def load_static_symbol_info(port):
#     fp = f'/data/cc/prod/symbol_info/{port.split(".")[1]}/{port.split(".")[0]}.json'
#     scfg = json.load(open(fp))
#     si = scfg['data'][-1][1]
#     return si


def timeit(f):
    @wraps(f)
    def inner(*args, **kw):
        s = time.time_ns()
        f(*args, **kw)
        e = time.time_ns()
        print(f'{f.__name__} finished in {e - s} nanoseconds.')
    return inner


