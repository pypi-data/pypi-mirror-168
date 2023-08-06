import os
from bdb import effective
import re
from pymongo import MongoClient,database,collection,operations
from collections import abc
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    NoReturn,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from bson.codec_options import CodecOptions
from bson.objectid import ObjectId
from bson.raw_bson import RawBSONDocument
from bson.son import SON
from bson.timestamp import Timestamp
from pymongo import ASCENDING, _csot, common, helpers, message
from pymongo.aggregation import (
    _CollectionAggregationCommand,
    _CollectionRawAggregationCommand,
)
from pymongo.bulk import _Bulk
from pymongo.change_stream import CollectionChangeStream
from pymongo.collation import validate_collation_or_none
from pymongo.command_cursor import CommandCursor, RawBatchCommandCursor
from pymongo.common import _ecc_coll_name, _ecoc_coll_name, _esc_coll_name
from pymongo.cursor import Cursor, RawBatchCursor
from pymongo.helpers import _check_write_command_response
from pymongo.message import _UNICODE_REPLACE_CODEC_OPTIONS
from pymongo.read_preferences import ReadPreference, _ServerMode
from pymongo.results import (
    BulkWriteResult,
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)
from pymongo.typings import _CollationIn, _DocumentIn, _DocumentType, _Pipeline
from pymongo.write_concern import WriteConcern
_FIND_AND_MODIFY_DOC_FIELDS = {"value": 1}
# Hint supports index name, "myIndex", or list of index pairs: [('x', 1), ('y', -1)]
_IndexList = Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]
_IndexKeyHint = Union[str, _IndexList]
_WriteOp = Union[operations.InsertOne,operations.DeleteOne,operations.DeleteMany,operations.ReplaceOne,operations.UpdateOne,operations.UpdateMany]

class ShardCollection(collection.Collection):
    def update_one(self, filter: Mapping[str, Any], update: Union[Mapping[str, Any], _Pipeline], upsert: bool = False, bypass_document_validation: bool = False, collation: Optional[_CollationIn] = None, array_filters: Optional[Sequence[Mapping[str, Any]]] = None, hint: Optional[_IndexKeyHint] = None, session: Optional["ClientSession"] = None, let: Optional[Mapping[str, Any]] = None, comment: Optional[Any] = None) -> UpdateResult:
        row=self.find_one(filter,{'_id':1})
        if row is not None:
            new_filter={"_id":row["_id"]}
            return super().update_one(new_filter, update, upsert, bypass_document_validation, collation, array_filters, hint, session, let, comment)

    def update_many(self, filter, update, upsert=False, array_filters=None, bypass_document_validation=False, collation=None, hint=None, session=None):
        rows=list(self.find(self,{'_id':1}))
        if rows is not None:
            new_filter={"_id":{"$in":rows}}
            return super().update_many(new_filter, update, upsert, array_filters, bypass_document_validation, collation, hint, session)

    def delete_one(self, filter: Mapping[str, Any], collation: Optional[_CollationIn] = None, hint: Optional[_IndexKeyHint] = None, session: Optional["ClientSession"] = None, let: Optional[Mapping[str, Any]] = None, comment: Optional[Any] = None) -> DeleteResult:
        row=self.find_one(filter,{'_id':1})
        if row is not None:
            new_filter={"_id":row["_id"]}
            return super().delete_one(new_filter, collation, hint, session, let, comment)

    def delete_many(self, filter, collation=None, hint=None, session=None):
        rows=list(self.find(self,{'_id':1}))
        if rows is not None:
            new_filter={"_id":{"$in":rows}}
            return super().delete_many(new_filter, collation, hint, session)

    def bulk_write(self, requests: Sequence[_WriteOp], ordered: bool = True, bypass_document_validation: bool = False, session: Optional["ClientSession"] = None, comment: Optional[Any] = None, let: Optional[Mapping] = None) -> BulkWriteResult:
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
        return super().bulk_write(new_request, ordered, bypass_document_validation, session, comment, let)

class ShardDatabase(database.Database):
    def __getitem__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        # print('shard db '+self.name)
        print('shard collection:'+self.name+'.'+name)
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
