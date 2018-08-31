from airflow.plugins_manager import AirflowPlugin
from mongo_plugin.hooks.mongo_hook import MongoHook
from mongo_plugin.operators.mongo_operator import MongoOperator


class MongoPlugin(AirflowPlugin):
    name = "MongoPlugin"
    operators = [MongoOperator]
    hooks = [MongoHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []