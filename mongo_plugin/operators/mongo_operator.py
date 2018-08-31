from airflow.models import BaseOperator
from mongo_plugin.hooks.mongo_hook import MongoHook

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

    def execute(self, context):
        """
        Executed by task_instance at runtime
        """
        mongo_conn = MongoHook(self.mongo_conn_id).get_conn()
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