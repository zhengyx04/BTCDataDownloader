import time
import urllib.request
import urllib.error
import urllib.parse
import config
import logging
from utils import log_exception
import traceback
import config
import threading
import datetime

class Broker(object):
    def __init__(self):
        self.name = self.__class__.__name__
        self.apikey = None
        self.secret = None

    def get_balance(self):
        pass

    def sell_order(self,currency_pair,price,qty, order_type):
        pass

    def buy_order(self,currency_pair,price,qty, order_type):
        pass

    def cancel_order(self,order_id):
        pass

    def get_open_orders(self):
        pass

    def with_draw(self,currency, qty, address):
        pass



class Market(object):
    registered_market={}
    def __init__(self):
        self.name = self.__class__.__name__
        self.depth_updated = 0
        self.update_rate = 1
        self.is_terminated = False

    def terminate(self):
        self.is_terminated = True #seems not used anywhere

    def get_depth(self):
        timediff = time.time() - self.depth_updated
        if timediff > self.update_rate:
            self.ask_update_depth()

        #order book is in valide if it updated time long time ago.
        timediff = time.time() - self.depth_updated
        if timediff > config.market_expiration_time:
            logging.warn('Market: %s order book is expired' % self.name)
            self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
                {'price': 0, 'amount': 0}]}
        return self.depth

    def gen_id(self,lu,currency_pair):
        return hex(int(lu.timestamp()*1e6))+currency_pair


    def convert_to_cny(self):
        if self.currency == "CNY":
            return
        for direction in ("asks", "bids"):
            for order in self.depth[direction]:
                order["price"] = self.fc.convert(order["price"], self.currency, "CNY")

    def start_websocket_depth(self):
        if config.SUPPORT_WEBSOCKET:
            t = threading.Thread(target = self.websocket_depth)
            t.start()

    def websocket_depth(self): #??
        import json
        from socketIO_client import SocketIO

        def on_message(data):
            data = data.decode('utf8')
            if data[0] != '2':
                return

            data = json.loads(data[1:])
            depth = data[1]

            logging.debug("depth coming: %s", depth['market'])
            self.depth_updated = int(depth['timestamp']/1000)
            self.depth = self.format_depth(depth)
        
        def on_connect():
            logging.info('[Connected]')

            socketIO.emit('land', {'app': 'haobtcnotify', 'events':[self.event]});

        with SocketIO(config.WEBSOCKET_HOST, port=config.WEBSOCKET_PORT) as socketIO:

            socketIO.on('connect', on_connect)
            socketIO.on('message', on_message)

            socketIO.wait()
    
    def ask_update_depth(self):
        try:
            self.update_depth()
            # self.convert_to_usd()
            self.depth_updated = time.time()
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logging.error("HTTPError, can't update market: %s" % self.name)
            traceback.print_exc()

            log_exception(logging.DEBUG)
        except Exception as e:
            logging.error("Can't update market: %s - %s" % (self.name, str(e)))
            log_exception(logging.DEBUG)
            traceback.print_exc()

    def get_ticker(self):
        depth = self.get_depth()
        res = {'ask':0, 'bid': 0}
        if len(depth['asks']) > 0 and len(depth["bids"]) > 0:
            res = {'date':depth['date'].strftime('%Y.%m.%d'),'lu':depth['lu'],'ask': depth['asks'][0],
                   'bid': depth['bids'][0]}
        return res

    ## Abstract methods
    def update_depth(self):
        pass

    def buy(self, price, amount):
        pass

    def sell(self, price, amount):
        pass

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x[0]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i[0]), 'amount': float(i[1])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['bids'], True)
        asks = self.sort_and_format(depth['asks'], False)
        return {'asks': asks, 'bids': bids}

    @staticmethod
    def get_market(name):
        return Market.registered_market[name]()

    @staticmethod
    def get_market_list():
        return Market.registered_market.keys()

    @staticmethod
    def register_market(class_name):
        name=class_name.__name__
        createfn=class_name.create
        if name in Market.registered_market:
            logging.info('conflicted market name for '+name+' will be skipped')
        else:
            Market.registered_market[name]=createfn;
            logging.info(name + ' is registered')


