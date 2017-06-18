import config
import urllib
import datetime
from .market import Market


class TemplateMarket(Market):
    def __init__(self):
        super().__init__()
        self.get_api_root_URL=''

    def get_exchange_depth(self,ticker):
        """
        :param ticker get order book from exchange and format the result
        :return: {'xt','asks':[{'price0','size0'},{'price1','size1'}],'bids':[{'price0','size0'},{'price1','size1'}]}
        """
        return {'xt':datetime.datetime.utcnow(),\
                'asks':[{'price':1000.0,'size':0.1},{'price':1001.0,'size':10}],\
                'bids':[{'price':999.0,'size':0.5},{'price':998.0,'size':1}]}

    def get_currency_pair(self,ticker):
        return 'pccy','occy'

    @staticmethod
    def create():
        return TemplateMarket()

Market.register_market(TemplateMarket)