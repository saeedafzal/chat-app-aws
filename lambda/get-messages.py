import json
import boto3
from boto3.dynamodb.conditions import Key

def _send_to_connection(data, event):
    id = event["requestContext"]["connectionId"]
    print(f"Connection ID: {id}")

    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url = "") # TODO: Set the http url from api gateway
    gatewayapi.post_to_connection(
        ConnectionId = id,
        Data = json.dumps(data).encode("utf-8")
    )

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    posts_table = dynamodb.Table("messages-db")

    data = posts_table.scan()
    print(data["Items"])

    _send_to_connection({ "messageType": "all_messages", "data": data["Items"] }, event)

    return {
        "statusCode": 200
    }