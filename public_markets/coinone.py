import json
import time
import base64
import hashlib
import hmac
import urllib
import datetime
from .market import Market

class Coinone(Market):
    def __init__(self):
      super().__init__()
      self.ACCESS_TOKEN = ''
      self.SECRET_KEY = ''
      self.urlapi = 'https://api.coinone.co.kr'

    def get_encoded_payload(self,payload):
      #add nonce
      payload[u'nonce'] = int(time.time()*1000)

      dumped_json = json.dumps(payload)
      encoded_json = base64.b64encode(dumped_json)
      return encoded_json

    def get_signature(self,encoded_payload, secret_key):
      signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
      return signature.hexdigest()

    def get_response(self,url,payload):
      encoded_payload = self.get_encoded_payload(payload)
      response = urllib.request.urlopen(self.urlapi+'url',
        format='json',
        data=encoded_payload,
        **{
          'X-COINONE-PAYLOAD': encoded_payload,
          'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, self.SECRET_KEY)
        })
      return json.loads(response.read().decode('utf8'))

    def get_order_book_ccy(self,occy):
        #occy can only be one of btc, eth, etc, xrp
        url = '/orderbook/?currency='
        res=urllib.request.urlopen(self.urlapi+url+occy).read().decode('utf8')
        return json.loads(res)

    def get_order_book(self):
        occy_list=['btc','eth','etc','xrp']
        return [self.get_order_book_ccy(e) for e in occy_list]

    def update_depth(self):
        depth=self.get_order_book()
        self.depth=[self.format_depth(e) for e in depth]

    def format_depth(self, depth):
        xt=datetime.datetime.utcfromtimestamp(float(depth['timestamp']))
        lu=datetime.datetime.utcnow()
        date=datetime.datetime.now().strftime('%Y.%m.%d')
        qv=True
        occy=depth['currency'].upper()
        pccy='KRW'
        _id=self.gen_id(lu,occy+'_'+pccy)
        return {'_id':_id,'date':date,'xt':xt,'lu':lu,'qv':qv,'occy':occy,'pccy':pccy,\
                'asks':self.__format_bidasks(depth['ask']),\
                'bids':self.__format_bidasks(depth['bid'])}

    def __format_bidasks(self,bidask):
        return [{'price':float(e['price']),'size':float(e['qty'])} for e in bidask]

    @staticmethod
    def create():
        return Coinone()

Market.register_market(Coinone)

if __name__   == "__main__":
    pass