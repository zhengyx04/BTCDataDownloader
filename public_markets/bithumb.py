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

    def __get_orderbook(self,param):
        return self.api.xcoinApiCall('/public/orderbook',param)

    def __get_recent_transaction(self):
        return self.api.xcoinApiCall('/public/recent_transactions', self.rgParams)

    def get_exchange_depth(self,ticker):
        occy,pccy=self.get_currency_pair(ticker)
        param={"order_currency" : occy.upper(), "payment_currency" : pccy.upper()}
        depth=self.__get_orderbook(param)
        return self.depth_transform(depth)


    def depth_transform(self, depth):
        res={'xt':datetime.datetime.utcfromtimestamp(float(depth['data']['timestamp'])/1e3)}
        res['asks'] = [{'price':float(e['price']),'size':float(e['quantity'])} for e in depth['data']['asks']]
        res['bids'] = [{'price':float(e['price']),'size':float(e['quantity'])} for e in depth['data']['bids']]
        return res

    @staticmethod
    def create():
        return Bithumb()

Market.register_market(Bithumb)