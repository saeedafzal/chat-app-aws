import json
import ast
import boto3

def _send_to_connection(message, connections):
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url = "") # TODO: Set the http url from api gateway
    
    for o in connections:
        gatewayapi.post_to_connection(
            ConnectionId = o["id"],
            Data = message
        )

def lambda_handler(event, context):
    message = event["body"]
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("connections-db")

    connections = table.scan()
    _send_to_connection(message, connections["Items"])

    message = ast.literal_eval(message)
    t = message.get("time")
    m = message.get("message")

    tb = dynamodb.Table("messages-db")
    tb.put_item(
        Item = {
            "id": f"id-{t}",
            "message": m,
            "time": t
        }
    )

    return {
        "statusCode": 200
    }