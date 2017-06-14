from .market import Market
from .__xcoin_api_client import XCoinAPI
import datetime


class Bithumb(Market):
    def __init__(self):
        super().__init__()
        self.api_key = "api_connect_key"
        self.api_secret = "api_secret_key"
        self.api = XCoinAPI(self.api_key,self.api_secret)
        self.rgParams = {"order_currency" : "BTC", "payment_currency" : "KRW"}

    def __get_ticker(self):
        return self.api.xcoinApiCall('/public/ticker',self.rgParams)

    def __get_recent_ticker(self):
        return self.api.xcoinApiCall('/public/recent_ticker',self.rgParams)

    def __get_orderbook(self):
        return self.api.xcoinApiCall('/public/orderbook',self.rgParams)

    def __get_recent_transaction(self):
        return self.api.xcoinApiCall('/public/recent_transactions', self.rgParams)

    def update_depth(self):
        depth=self.__get_orderbook()
        self.depth=self.format_depth(depth)

    def format_depth(self, depth):
        xt=datetime.datetime.utcfromtimestamp(float(depth['data']['timestamp'])/1e3)
        date=datetime.datetime.now().date().strftime('%Y.%m.%d')
        lu=datetime.datetime.utcnow()
        occy=depth['data']['order_currency'].upper()
        pccy=depth['data']['payment_currency'].upper()
        _id=self.gen_id(lu,occy+'_'+pccy)
        return {'_id':_id,'date':date,'xt':xt,'lu':lu,'qv':True,'occy':occy,'pccy':pccy, \
                'asks':self.__format_bidasks(depth['data']['asks']),\
                'bids':self.__format_bidasks(depth['data']['bids'])}

    def __format_bidasks(self,bidask):
        return [{'price':float(e['price']),'size':float(e['quantity'])} for e in bidask]

    @staticmethod
    def create():
        return Bithumb()

Market.register_market(Bithumb)