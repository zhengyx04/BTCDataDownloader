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
      self.AIPKey = self.get_config('APIKey')
      self.Secret = self.get_config('Secret')
      self.urlapi = 'https://api.coinone.co.kr'
      self.get_api_url_orderbook='https://api.coinone.co.kr/orderbook/?currency={ticker:s}'

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

    def get_exchange_depth(self,ticker):
        #occy can only be one of btc, eth, etc, xrp
        url = self.get_api_url_orderbook.format(ticker=ticker)
        res=urllib.request.urlopen(url).read().decode('utf8')
        res=json.loads(res)
        return self.depth_transform(res)

    def depth_transform(self, depth):
        xt=datetime.datetime.utcfromtimestamp(float(depth['timestamp']))
        res={'xt':xt}
        res['asks']=[{'price':e['price'],'size':e['qty']} for e in depth['ask']]
        res['bids'] = [{'price': e['price'], 'size': e['qty']} for e in depth['bid']]
        return res

    @staticmethod
    def create():
        return Coinone()

Market.register_market(Coinone)

if __name__   == "__main__":
    pass