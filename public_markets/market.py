import time
import urllib.request
import urllib.error
import urllib.parse
import logging
from utils import log_exception
import traceback
import datetime
import config

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
        self.__init_config()
        self.depth_updated = 0
        self.is_terminated = False
        self.update_success = False

    def terminate(self):
        self.is_terminated = True #terminate update

    def __init_config(self):
        def get_config(attribution):
            return config.get_market_config(self.name,attribution)
        self.get_config = get_config
        self.update_rate = self.get_config('UpdateRate')
        self.tickerlist = self.get_config('TickerList')

    def get_depth(self):
        self.update_success = False
        timediff = time.time() - self.depth_updated
        if timediff > self.update_rate:
            self.ask_update_depth()

        #order book is in valide if it updated time long time ago.
        timediff = time.time() - self.depth_updated
        if timediff > config.market_expiration_time:
            logging.warn('Market: %s order book is expired' % self.name)
            self.update_success = False

        return self.depth if self.update_success else None

    def gen_id(self,lu,ticker):
        return hex(int(lu.timestamp()*1e6))+ticker

    def ask_update_depth(self):
        try:
            self.update_depth()
            self.depth_updated = time.time()
            self.update_success = True
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logging.error("HTTPError, can't update market: %s" % self.name)
            traceback.print_exc()
            log_exception(logging.DEBUG)
        except Exception as e:
            logging.error("Can't update market: %s - %s" % (self.name, str(e)))
            log_exception(logging.DEBUG)
            traceback.print_exc()

    def update_depth(self):
        self.depth = [self.update_depth_core(ticker) for ticker in self.tickerlist]

    def update_depth_core(self, ticker):
        """
        get depth and store it in a dictionary, if has more than 1 tickers, store them in a  list
        """
        try:
            depth = self.get_exchange_depth(ticker)
            return self.format_depth(depth, ticker)
        except:
            logging.error('load data error for ticker: '+ticker)

    def format_depth(self,depth,ticker):
        if not all(k in depth for k in ('xt', 'asks', 'bids')):
            raise Exception('invalid format from get_exchnage_depth')
        depth['date'] = datetime.datetime.now().date().strftime('%Y.%m.%d')
        depth['lu'] = datetime.datetime.utcnow()
        depth['_id'] = self.gen_id(depth['lu'], ticker)
        occy,pccy = self.get_currency_pair(ticker)
        depth['pccy'] = pccy
        depth['occy'] = occy
        depth['sym'] = ticker
        depth['asks'] = sorted(depth['asks'],key=lambda x:x['price'],reverse=False)
        depth['bids'] = sorted(depth['bids'], key=lambda x: x['price'], reverse=True)
        return depth

    ## Abstract methods
    def get_currency_pair(self,ticker):
        pass

    def get_exchange_depth(self,ticker):
        return {}

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