import os
from pymongo import MongoClient,database,collection,operations

class ShardCollection(collection.Collection):
    def update_one(self, filter, update, upsert=False, bypass_document_validation=False, collation=None, array_filters=None, hint=None, session=None):
        row=self.find_one(filter,{'_id':1})
        if row is not None:
            new_filter={"_id":row["_id"]}
            return super().update_one(new_filter, update, upsert, bypass_document_validation, collation, array_filters, hint, session)
    
    def update_many(self, filter, update, upsert=False, array_filters=None, bypass_document_validation=False, collation=None, hint=None, session=None):
        rows=list(self.find(self,{'_id':1}))
        if rows is not None:
            new_filter={"_id":{"$in":rows}}
            return super().update_many(new_filter, update, upsert, array_filters, bypass_document_validation, collation, hint, session)

    def delete_one(self, filter, collation=None, hint=None, session=None):
        row=self.find_one(filter,{'_id':1})
        if row is not None:
            new_filter={"_id":row["_id"]}
            return super().delete_one(new_filter, collation, hint, session)


    def delete_many(self, filter, collation=None, hint=None, session=None):
        rows=list(self.find(self,{'_id':1}))
        if rows is not None:
            new_filter={"_id":{"$in":rows}}
            return super().delete_many(new_filter, collation, hint, session)

    def bulk_write(self, requests, ordered=True, bypass_document_validation=False, session=None):
        new_request=[]
        for request in requests:
            if type(request) is operations.UpdateOne or type(request) is operations.DeleteOne or type(request) is operations.ReplaceOne:
                row=self.find_one(request._filter,{'_id':1})
                if row is not None:
                    new_filter={"_id":row["_id"]}
                    request._filter=new_filter
                    print(request)
                    new_request.append(request)
            elif type(request) is operations.UpdateMany or type(request) is operations.DeleteMany:
                rows=list(self.find(request._filter,{'_id':1}))
                if rows is not None:
                    new_filter={"_id":{"$in":rows}}
                    request._filter=new_filter
                    print(request)
                    new_request.append(request)
            else:
                new_request.append(request)
        return super().bulk_write(new_request, ordered, bypass_document_validation, session)

class ShardDatabase(database.Database):
    def __getitem__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        # print('shard db '+self.name)
        # print('shard collection:'+self.name+'.'+name)
        try:
            if name !='admin' and os.getenv(self.name+'.'+name,None) is None:
                os.environ[self.name+'.'+name]="1"
                self.client.admin.command('shardcollection', self.name+'.'+name, key={'_id': 1})
        except Exception as  ex:
            print(ex)
        return ShardCollection(self,name)

class ShardMongoClient(MongoClient):
    #This attribute interceptor works when we call the class attributes.
    def __getitem__(self, name):
        # print('shard '+name)
        try:
            if name !='admin' and os.getenv(name,None) is None:
                os.environ[name]="1"
                db_admin = self.get_database('admin')
                db_admin.command('enablesharding', name)
        except Exception as  ex:
            print(ex)
        return ShardDatabase(self,name)
