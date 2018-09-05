# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from datetime import datetime, timedelta
from airflow.operators import (GetWorkflowOperator, GetWorkflowDocsOperator)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 8, 31),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('test_workflow_xcom', default_args=default_args)


t1 = GetWorkflowOperator(task_id='get_workflow',
                               mongo_conn_id="mongo_default",
                               mongo_database = "karakuri",
                               mongo_colletion = "workflows",
                               mongo_query = {"name": "SFSC review: new"},
                               dag=dag)

t2 = GetWorkflowDocsOperator(task_id='get_workflow_docs',
                             provide_context=True,
                             mongo_conn_id="mongo_default",
                             dag=dag)

t2.set_upstream(t1)