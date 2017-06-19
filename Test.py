import public_markets
if __name__=='__main__':
    print(public_markets.Market.get_market_list())
    mkt=public_markets.Market.get_market('Kraken')
    mkt.get_depth()
    #print(mkt.get_depth())