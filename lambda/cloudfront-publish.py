import json
import boto3
import time

def lambda_handler(event, context):
    allFiles = ["/*"]
    client = boto3.client("cloudfront")
    invalidation = client.create_invalidation(
        DistributionId="", # ID of cloudfront distribution
        InvalidationBatch={
            "Paths": {
                "Quantity": 1,
                "Items": allFiles
            },
            "CallerReference": str(time.time())
        }
    )
    
    pipeline = boto3.client("codepipeline")
    response = pipeline.put_job_success_result(
        jobId=event["CodePipeline.job"]["id"]
    )

    return { "statusCode": 200 }