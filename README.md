# Distributed Systems - Chat App

https://www.loom.com/share/d97204007a7543d5ac99e83aa1c08a0d

These are the steps needed to recreate the chat application created in the video linked above.

## Repository
In the `/static` folder of this repository, there is the code for the web application, including the html, css and JavaScript files. You can fork this repository
or create your own in **CodeCommit** and copy these files over there.

## S3 & CloudFront
 - Create an S3 bucket to hold the static files
 - Set the property to allow static file hosting
 - Add the policy (replace `<bucket-name>` with the name of the bucket you created):
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<bucket-name>/*"
        }
    ]
}
```
 - Create a cloudfront distribution, setting the origin ID to be the URL of the static S3 site.
 - Select `redirect HTTP to HTTPS`
 - Create the distribution

## AWS Lambda
 - In the `/lambda` folder, there are *python* files.
 - Create a lambda function for each of those files, set the name of the function as the filename.
 - Copy the code into the lambda function.
 - Save the function.

**Do this for each of the files**

## Code Pipeline
 - Create a new pipeline.
 - For the source, set it to the repository where the web files in the `/static` folder is, either in **CodeCommit** or you can use your own **GitHub** repository.
 - Skip build stages.
 - Create the pipeline.
 - Click edit on the pipeline page and add a stage
 - Set the action to be the `cloudfront-publish` lambda that you created in the previous steps

**The CD pipeline should be setup now.**

## DynamoDB
 - Create 2 tables in dynamoDB
   - A table to hold connection Ids
   - Another table to hold all the messages
   
## API Gateway
 - Create a WebSocket API
 - Set the default routes to lambdas created in the previous steps:
   - For `$connect` -> Trigger the lambda `on-connect`
   - For `$disconnect` -> Trigger the lambda `on-disconnect`
 - Create a route for `get_messages` and `send_message`
 - Set the lambda trigger for `get_messages` to the function `get-messages`
 - Set the lambda trigger for `send_message` to the function `broadcast`
 - Make sure to click on deploy API so you can see the URLs on the websocket.
   - You will need to edit the lambdas for `broadcast` and `get-messages` to change the *TODO* comment in the script to be the http link generated
   - Also, in the JavaScript file, under the *TODO*, add the websocket URL.
   
**This should allow you to have a working chat application.**

## Resources
https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteAccessPermissionsReqd.html
https://aws.amazon.com/blogs/compute/announcing-websocket-apis-in-amazon-api-gateway/
https://medium.com/@yagonobre/automatically-invalidate-cloudfront-cache-for-site-hosted-on-s3-3c7818099868
https://medium.com/@likhita507/real-time-chat-application-using-webscockets-in-apigateway-e3ed759c4740
https://medium.com/swlh/real-time-chat-application-with-aws-websockets-7f06b833f02c
https://hackernoon.com/websockets-api-gateway-9d4aca493d39
