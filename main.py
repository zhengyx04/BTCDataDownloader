import logging
import glob
import public_markets
import os
import inspect
import config
import threading
import datetime
import DataBase

class MarketDataLoader(object):
    def __init__(self,db):
        self.inject_verbose_info()
        self.is_terminate=False
        self.db=db

    def inject_verbose_info(self):
        logging.VERBOSE = 15
        logging.verbose = lambda x: logging.log(logging.VERBOSE, x)
        logging.addLevelName(logging.VERBOSE, "VERBOSE")

    @staticmethod
    def list_public_marketsold(if_print=True):
        logging.debug('list_markets')
        for filename in glob.glob(os.path.join(public_markets.__path__[0], "*.py")):
            module_name = os.path.basename(filename).replace('.py', '')
            if not module_name.startswith('_'):
                module = __import__("public_markets." + module_name)
                test = eval('module.' + module_name)
                if if_print:
                    for name, obj in inspect.getmembers(test):
                        if inspect.isclass(obj) and 'Market' in (j.__name__ for j in obj.mro()[1:]):
                            if not obj.__module__.split('.')[-1].startswith('_'):
                                print(obj.__name__)
        sys.exit(0)

    @staticmethod
    def list_public_market():
        for market in public_markets.Market.registered_market:
            print(market)
        sys.exit(0)

    def init_logger(self, args):
        level = logging.INFO
        if args.verbose:
            level = logging.VERBOSE
        if args.debug:
            level = logging.DEBUG
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                            level=level)

        Rthandler = RotatingFileHandler('arbitrage.log', maxBytes=100*1024*1024,backupCount=10)
        Rthandler.setLevel(level)
        formatter = logging.Formatter('%(asctime)-12s [%(levelname)s] %(message)s')
        Rthandler.setFormatter(formatter)
        logging.getLogger('').addHandler(Rthandler)

        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--debug", help="debug verbose mode",
                            action="store_true")
        parser.add_argument("-v", "--verbose", help="info verbose mode",
                            action="store_true")
        parser.add_argument("-m", "--markets", type=str,
                            help="markets, example: -mHaobtcCNY,Bitstamp")
        parser.add_argument("-s", "--status", help="status", action="store_true")

        parser.add_argument("command", nargs='*', default="watch",
                            help='verb: "watch|list-public-markets|save-depth-info"')
        args = parser.parse_args()
        self.init_logger(args)
        self.exec_command(args)

    def exec_command(self,args):
        logging.debug('exec_command:%s' % args)
        if "watch" in args.command:
            self.display_depth_info(args.markets)
        if "list-public-markets" in args.command:
            MarketDataLoader.list_public_markets()
        if "save-depth-info" in args.command:
            self.save_depth_info(args.markets)

    def dispaly_depth_info(self,markets):
        self.markets=self.init_markets(markets)
        self.__display_depth_info()


    def __display_depth_info(self):
        if not self.is_terminate:
            threading.Timer(config.refresh_rate,self.__display_depth_info).start()
        print('Get data at: ',datetime.datetime.utcnow())
        for market in self.markets:
            depth=market.get_depth()
            print('get data from ', market.name, end='')
            print(depth)

    def init_markets(self,markets):
        return [public_markets.Market.get_market(e) for e in markets]

    def save_depth_info(self,markets):
        self.markets=self.init_markets(markets)
        self.__save_depth_info()

    def __save_depth_info(self):
        if not self.is_terminate:
            threading.Timer(config.refresh_rate,self.__save_depth_info).start()
        print('fetching data at: ', datetime.datetime.now())
        for market in self.markets:
            depth=market.get_depth()
            self.db.insert(market.name, depth)
            print('save data from ', market.name, end='')
            print(depth)

if __name__=='__main__':
    db=DataBase.MongoDB('localhost',8001)

    marketDownload=MarketDataLoader(db)
    #marketDownload.dispaly_depth_info(['PoloniexUSD'])
    marketDownload.save_depth_info(['Coinone'])
    #mkt=public_markets.Market.get_market('PoloniexUSD')
    #mkt.get_depth()

if __name__=='__main__2':
    mkt=public_markets.Market.get_market('Bithumb')
    mkt.update_depth()

