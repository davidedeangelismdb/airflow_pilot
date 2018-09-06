from airflow.plugins_manager import AirflowPlugin
from mongo_plugin.hooks.mongo_hook import MongoHook
from mongo_plugin.operators.get_workflow import GetWorkflowOperator
from mongo_plugin.operators.get_workflow_docs import GetWorkflowDocsOperator
from mongo_plugin.operators.transform_doc_to_task import TransformDocToTaskOperator


class MongoPlugin(AirflowPlugin):
    name = "MongoPlugin"
    operators = [GetWorkflowOperator,
                 GetWorkflowDocsOperator,
                 TransformDocToTaskOperator]
    hooks = [MongoHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []