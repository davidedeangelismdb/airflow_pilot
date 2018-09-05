import logging
import datetime
import bson
import bson.json_util
from airflow.models import BaseOperator
from pymongo.errors import PyMongoError
from mongo_plugin.hooks.mongo_hook import MongoHook
from support import common
from support.db.supportissue import SupportIssue

logger = logging.getLogger(__name__)

class MongoOperator(BaseOperator):

    def __init__(self,
                 mongo_conn_id,
                 mongo_database = 'test',
                 mongo_colletion = 'colls',
                 mongo_query = {},
                 *args, **kwargs):
        super(MongoOperator, self).__init__(*args, **kwargs)
        # Conn Ids
        self.mongo_conn_id = mongo_conn_id
        self.mongo_database = mongo_database
        self.mongo_colletion = mongo_colletion
        self.mongo_query = mongo_query
        self.mongo_conn = MongoHook(self.mongo_conn_id).get_conn()
        #karakuri collections
        self.coll_queue = self.mongo_conn.get_database('karakuri').get_collection('queue')
        self.coll_users = self.mongo_conn.get_database('karakuri').get_collection('users')
        self.coll_issues = self.mongo_conn.get_database('support').get_collection('issues')
        self.coll_workflows = self.mongo_conn.get_database('karakuri').get_collection('workflows')

    def execute(self, context):
        """
        Executed by task_instance at runtime
        """
        mongo_conn = self.mongo_conn
        collection = mongo_conn.get_database(self.mongo_database).get_collection(self.mongo_colletion)
        cursor = collection.find(self.mongo_query)
        result = self.transform(cursor)
        print("RESULT FIND DB: {}, COLLECTION: {}, QUERY: {}, RESULT: {}".format(self.mongo_database, self.mongo_colletion, self.mongo_query, result))


    def transform(self, docs):
        """
        Processes pyMongo cursor and returns single array with each element being
                a JSON serializable dictionary
        MongoToS3Operator.transform() assumes no processing is needed
        ie. docs is a pyMongo cursor of documents and cursor just needs to be
            converted into an array.
        """
        return [doc for doc in docs]

