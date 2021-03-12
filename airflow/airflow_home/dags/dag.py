from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Binh Phan',
    'depends_on_past': False,
    'start_date': days_ago(31),
    'email': ['example@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

#instantiates a directed acyclic graph
dag = DAG(
    'ml_pipeline',
    default_args=default_args,
    description='A Machine Learning pipeline',
    schedule_interval=timedelta(days=30),
)

train = BashOperator(
    task_id='train',
    depends_on_past=False,
    bash_command='python3 ../../../src/train.py',
    retries=3,
    dag=dag,
)

predict = BashOperator(
    task_id='predict',
    depends_on_past=False,
    bash_command='python3 ../../../src/predict.py',
    retries=3,
    dag=dag,
)

train >> predict
