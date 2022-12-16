from pprint import pprint

from src.services.aws.ws import post_to_connection
from src.tasks.dummy_task import DummyTask

task_map = {
    "dummy": DummyTask
}


def handler(event, context):
    pprint(event)
    task_name = event['task_name']
    payload = event["payload"]
    conn_id = event["conn_id"]
    print(f"Running task '{task_name}'({payload}) for client {conn_id}")
    task = task_map.get(task_name)
    if not task:
        return {"statusCode": 200, "body": f"task {task_name} not found"}

    result = task.run(payload)
    post_to_connection(conn_id, {"result": result})
    return {"statusCode": 200, "body": "OK"}
