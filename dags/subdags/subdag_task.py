# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from airflow.models import DAG
from airflow.operators import (DummyOperator, ProcessTaskOperator)
from mongo_plugin.hooks.mongo_hook import MongoHook

def subdag_tasks(parent_dag_name, child_dag_name, args):
    dag_subdag = DAG(
        dag_id='%s.%s' % (parent_dag_name, child_dag_name),
        default_args=args,
        schedule_interval="@daily",
    )

    mongo_conn = MongoHook('mongo_default').get_conn()

    workflow = mongo_conn.get_database('karakuri').get_collection('workflows').find_one({"name": "SFSC review: new airflow"})
    workflow_id = workflow.get('_id')
    tasks = mongo_conn.get_database('karakuri').get_collection('queue').find({"active": True, "approved": True, "inProg": False, "done": False, "approvedBy": "karakuri", "workflow": workflow_id})

    #static creation of known number of tasks option, reading the db generate perf issue which makes
    # impossible to parallelise the subdagging
    # tasks = [{'key': '001234567'},{'key': '001234567'},{'key': '001234567'}]

    for task in tasks:
        ProcessTaskOperator(
            task_id='%s-task-%s' % (child_dag_name, task.get('key', 'error')),
            mongo_conn_id="mongo_default",
            mongo_database = "karakuri",
            mongo_colletion = "workflows",
            task = task,
            dag=dag_subdag)

    return dag_subdag