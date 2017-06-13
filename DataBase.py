import pymongo

class MongoDB(object):
    def __init__(self,host,port):
        self.client=pymongo.MongoClient(host,port)
        self.db=self.client.BTCMarketDepth

    def insert(self,market,documents):#each market will be a collection
        if type(documents)==list:
            for d in documents:
                self.db[market].insert_one(d)
        else:
            self.db[market].insert_one(documents)

    def update(self,market, document):
        _id=document['_id']
        document.pop('_id')
        self.db[market].update({'_id':_id},{'$set':document},upsert=False)
    def get_collection(self,market):
        return self.db[market]

    def delete(self,market,_id):
        result = self.db[market].delete_one({'_id':ObjectId(_id)})
        return result
    def clear_market_data(self,market):
        self.db[market].drop()
        print('removed data for ',market, ' from database')

    def get_market_list(self):
        return self.db.collection_names()

if __name__=='__main__':
    db=MongoDB('localhost',8001)