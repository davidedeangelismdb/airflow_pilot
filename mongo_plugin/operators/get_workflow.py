import logging
from airflow.models import BaseOperator
from mongo_plugin.hooks.mongo_hook import MongoHook

logger = logging.getLogger(__name__)

class GetWorkflowOperator(BaseOperator):


    def __init__(self,
                 mongo_conn_id,
                 mongo_database = 'test',
                 mongo_colletion = 'colls',
                 mongo_query = {},
                 *args, **kwargs):
        super(GetWorkflowOperator, self).__init__(*args, **kwargs)
        # Conn Ids
        self.mongo_conn_id = mongo_conn_id
        self.mongo_database = mongo_database
        self.mongo_colletion = mongo_colletion
        self.mongo_query = mongo_query
        self.mongo_conn = MongoHook(self.mongo_conn_id).get_conn()

    def execute(self, context):
        collection = self.mongo_conn.get_database(self.mongo_database).get_collection(self.mongo_colletion)
        result = collection.find_one(self.mongo_query)
        return result

