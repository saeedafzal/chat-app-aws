import json
import boto3

def lambda_handler(event, context):
    id = event["requestContext"]["connectionId"]

    dynamodb = boto3.resource("dynamodb")
    posts_table = dynamodb.Table("connections-db")
    
    posts_table.put_item(
        Item = {
            "id": id
        }
    )

    return {
        "statusCode": 200,
    }