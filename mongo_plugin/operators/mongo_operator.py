from airflow.models import BaseOperator
from mongo_plugin.hooks.mongo_hook import MongoHook

class MongoOperator(BaseOperator):

    def __init__(self, mongo_conn_id,*args, **kwargs):
        super(MongoOperator, self).__init__(*args, **kwargs)
        # Conn Ids
        self.mongo_conn_id = mongo_conn_id

    def execute(self, context):
        """
        Executed by task_instance at runtime
        """
        mongo_conn = MongoHook(self.mongo_conn_id).get_conn()
        print(mongo_conn)

    def transform(self, docs):
        """
        Processes pyMongo cursor and returns single array with each element being
                a JSON serializable dictionary
        MongoToS3Operator.transform() assumes no processing is needed
        ie. docs is a pyMongo cursor of documents and cursor just needs to be
            converted into an array.
        """
        return [doc for doc in docs]