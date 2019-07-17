import json
import logging
import boto3

dynamodb_table_name = "test-s3-file-contents"
s3_bucket_name = "rorlovskyi-temp-files"


def lambda_handler(event, context):

    s3 = boto3.client('s3')
    """ :type: pyboto3.s3"""

    dynamodb = boto3.client('dynamodb')
    """:type: pyboto3.dynamodb"""

    file_name = event["Records"][0]["s3"]["object"]["key"]
    size = event["Records"][0]["s3"]["object"]["size"]

    file_object = s3.get_object(Bucket=s3_bucket_name, Key=file_name)
    body = file_object['Body'].read().decode('utf-8')

    item = {
        "fileName": {
            "S": file_name,
        },
        "fileContent": {
            "S": body
        },
        "fileSize": {
            "N": str(size)
        }
    }

    return dynamodb.put_item(
        TableName=dynamodb_table_name,
        Item=item
    )