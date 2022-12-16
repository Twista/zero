from src.services.aws.ws import post_to_connection


def connect(event, context):
    conn_id = event['requestContext']['connectionId']

    print(f"Connection: {conn_id} created!")

    resp = post_to_connection(conn_id, {"conn_id": conn_id})
    print(resp.status_code)
    print(resp.text)
    return {"statusCode": 200, "body": 'Connected.'}
