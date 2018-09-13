# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from datetime import datetime, timedelta
from airflow.operators import (GetWorkflowOperator, GetWorkflowDocsOperator, TransformDocToTaskOperator, PythonOperator, QueueTaskOperator, TriggerDagRunOperator)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 9, 13),
    'schedule_interval': '@daily',
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('sfsc_review_new_airflow', default_args=default_args)


def conditionally_trigger(context, dag_run_obj):
    """This function decides whether or not to Trigger the remote DAG"""
    c_p = context['params']['condition_param']
    print("Controller DAG : conditionally_trigger = {}".format(c_p))
    value = context['task_instance'].xcom_pull(task_ids=c_p)
    print("pull_docs: ", value)
    if value:
        return dag_run_obj

t1 = GetWorkflowOperator(task_id='get_workflow_by_name',
                               mongo_conn_id="mongo_default",
                               mongo_database = "karakuri",
                               mongo_colletion = "workflows",
                               mongo_query = {"name": "substitut_actual_workflow_name"},
                               dag=dag)

t2 = GetWorkflowDocsOperator(task_id='execute_workflow_query',
                             provide_context=True,
                             mongo_conn_id="mongo_default",
                             dag=dag)

t3 = TransformDocToTaskOperator(task_id='transform_query_result_to_tasks',
                                provide_context=True,
                                mongo_conn_id="mongo_default",
                                dag=dag)

t4 = QueueTaskOperator(task_id='save_tasks',
                       provide_context=True,
                       mongo_conn_id="mongo_default",
                       dag=dag)

t5 = TriggerDagRunOperator(task_id='trigger_sfsc_review_new_airflow_process_tasks',
                           trigger_dag_id="sfsc_review_new_airflow_process_tasks",
                           python_callable=conditionally_trigger,
                           params={'condition_param': 'save_tasks'},
                           dag=dag)

t1 >> t2 >> t3 >> t4 >> t5