import logging
from airflow.models import BaseOperator
from mongo_plugin.hooks.mongo_hook import MongoHook
from karakuri import Karakuri
from support.jira.jirapp import Jirapp, JirappException
from support.sfdc.sfdcpp import Sfdcpp, SfdcppException

logger = logging.getLogger(__name__)

class ProcessTaskOperator(BaseOperator):

    def __init__(self,
                 mongo_conn_id,
                 mongo_database = 'test',
                 mongo_colletion = 'colls',
                 mongo_query = {},
                 task = None,
                 *args, **kwargs):
        super(ProcessTaskOperator, self).__init__(*args, **kwargs)
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
        #
        self.task = task

    def execute(self, context):
        print("CONTEXT: ", context)
        print("TASK TO PROCESS: ", self.task)
        karakuri = self.get_karakuri()
        result = None
        if self.task:
            try:
                result = karakuri.processTask(self.task.get('_id'), approvedOnly=True, userDoc=self.authentincate())
            except Exception as e:
                logger.error("Failed to queue task: %s", str(e))

        print("RESULTS: ", result)
        #return result


    def authentincate(self):
        try:
            user = self.coll_users.find_one({'user': 'a_user'})
            return user
        except Exception:
            logger.error("Abort - Failed to read users collection")


    def get_karakuri(self):
        args = self.create_args()
        jira = Jirapp(args, self.mongo_conn)
        jira.set_live(args['live'])
        # Initialize SFDC++
        sfdc = Sfdcpp(args['sfdc_username'], args['sfdc_password'],
                      args['sfdc_server'], args['sfdc_schemaversion'])
        sfdc.set_live(args['live'])
        # Set the Issuer. There can be only one:
        # https://www.youtube.com/watch?v=sqcLjcSloXs
        issuer = jira
        user = {'sudoUser': 'a_sudo_user'}

        print("CREATE KARAKURI")
        karakuri = Karakuri(args, jira, sfdc, issuer, self.mongo_conn)

        return karakuri

    def create_args(self):
        cert = bytes("RSA PRIVATE KEY", "utf-8").decode("unicode_escape")
        args = {'live': False,
                'jira_key_cert': cert,
                'jira_access_token': 'jira_access_token',
                'jira_access_token_secret': 'jira_access_token_secret',
                'jira_consumer_key': 'jira_consumer_key',
                'jira_server': "jira_server",
                'sfdc_username': 'sfdc_username',
                'sfdc_password': 'sfdc_password',
                'sfdc_server': "sfdc_server",
                'sfdc_schemaversion': "35.0",
                'log_level': 'DEBUG',
                'log': '/home/root/airflow/logs'}
        return args

    def transform(self, docs):
        """
        Processes pyMongo cursor and returns single array with each element being
                a JSON serializable dictionary
        MongoToS3Operator.transform() assumes no processing is needed
        ie. docs is a pyMongo cursor of documents and cursor just needs to be
            converted into an array.
        """
        return [doc for doc in docs]