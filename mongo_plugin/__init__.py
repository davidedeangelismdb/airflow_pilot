from airflow.plugins_manager import AirflowPlugin
from mongo_plugin.hooks.mongo_hook import MongoHook
from mongo_plugin.operators.mongo_operator import MongoOperator
from mongo_plugin.operators.findworflowdocs_operator import FindWorkflowsDocsOperator
from mongo_plugin.operators.get_workflow import GetWorkflowOperator
from mongo_plugin.operators.get_workflow_docs import GetWorkflowDocsOperator



class MongoPlugin(AirflowPlugin):
    name = "MongoPlugin"
    operators = [MongoOperator, FindWorkflowsDocsOperator, GetWorkflowOperator, GetWorkflowDocsOperator]
    hooks = [MongoHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []