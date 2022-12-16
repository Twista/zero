from flask import request
from flask.blueprints import Blueprint

from src.services.aws.awslambda import exec_async

bp = Blueprint("task-api", __name__, url_prefix="/tasks")


@bp.route("/create-task", methods=["POST"])
def create_task():
    body = request.get_json()
    print(body)
    conn_id = body.get("conn_id")

    exec_async("task_runner", {"conn_id": conn_id, "task_name": "dummy", "payload": "hello"})
    return {"status": "OK"}, 200
