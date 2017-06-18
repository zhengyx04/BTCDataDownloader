from .market import Market
import urllib
import json
import datetime
import numpy as np
from dateutil.relativedelta import relativedelta

#future exchange
class BitmexFuture(Market):
    def __init__(self):
        super().__init__()
        self.URLAPI=u'https://www.bitmex.com/api/v1/orderBook/L2?symbol={symbol:s}&depth={depth:d}'
        self.future_list=['XBT','ETH']
        self.future_month_map = {3:'H',6:'M',9:'U',12:'Z'}

    def update_depth(self):
        self.depth=[self._update_depth(sym) for sym in self.get_contract_symbols()]

    def get_contract_front_back_month(self):
        date=datetime.datetime.now().date()
        month=date.month
        front_year=date.year
        front_month=int(np.ceil(month/3))*3
        back_month_date=datetime.date(date.year,front_month,1)+relativedelta(months=3)
        back_year=back_month_date.year
        back_month=back_month_date.month
        return [self.future_month_map[front_month]+str(front_year)[-2:], \
                self.future_month_map[back_month] + str(back_year)[-2:]]

    def get_contract_symbols(self):
        return [ sym+month_sym for sym in self.future_list for month_sym in self.get_contract_front_back_month()]

    def _update_depth(self,sym):
        xt=datetime.datetime.utcnow()
        query_str=self.URLAPI.format(symbol=sym,depth=20)
        ret=urllib.request.urlopen(query_str).read().decode('utf8')
        ret=json.loads(ret)
        ret=self._format_depth(sym, xt,ret)
        return ret

    def _format_depth(self,sym, xt, depth):
        lu=datetime.datetime.utcnow()
        date=datetime.datetime.now().date().strftime('%Y.%m.%d')
        qv = True
        occy = 'BTC'
        pccy = 'USD'
        prod_type = 'future'
        _id=self.gen_id(lu,sym)
        ret={'_id':_id,'date':date,'xt':xt,'lu':lu,'ticker':sym,'qv':qv,'occy':occy,'pccy':pccy,\
             'type':prod_type,'asks':self._format_bid_ask(depth,'Sell',is_ascending=True),\
            'bids':self._format_bid_ask(depth,'Buy',is_ascending=False)}
        return ret

    def _format_bid_ask(self,bid_ask,side,is_ascending=True):
        return sorted([{'price':e['price'],'size':e['size']} for e in bid_ask if e['side']==side],key=lambda x:x['price'],reverse=(not is_ascending))

    @staticmethod
    def create():
        return BitmexFuture()

Market.register_market(BitmexFuture)


class BitmexIndex(Market):
    def __init__(self):
        pass


