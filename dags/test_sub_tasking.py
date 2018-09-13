# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from datetime import datetime, timedelta
from mongo_plugin.hooks.mongo_hook import MongoHook
from airflow.operators import (DummyOperator, SubDagOperator)
from subdags.subdag_task import subdag_tasks

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 9, 12)
}

mongo_conn = MongoHook('mongo_default').get_conn()

workflow = mongo_conn.get_database('karakuri').get_collection('workflows').find_one({"name": "substituto_real_workflow_name"})
workflow_id = workflow.get('_id')
tasks = mongo_conn.get_database('karakuri').get_collection('queue').find({"active": True, "approved": True, "inProg": False, "done": False, "approvedBy": "karakuri", "workflow": workflow_id})

print("TASKS: ", tasks)

dag = DAG('sfsc_review_new_airflow_process_tasks',
          default_args=default_args,
          schedule_interval=None
          )

start = DummyOperator(
    task_id='start',
    default_args=default_args,
    dag=dag
)

process = SubDagOperator(
    task_id='process',
    subdag=subdag_tasks('sfsc_review_new_airflow_process_tasks', 'process', tasks, default_args),
    default_args=default_args,
    dag=dag,
)

start >> process
