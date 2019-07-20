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

    rows = body.split()

    return rows

    # write records to dynamo db
    # tokens = csv.reader(csv_file, delimiter=args.delimiter)
    # # read first line in file which contains dynamo db field names
    # header = tokens.next();
    # # read second line in file which contains dynamo db field data types
    # headerFormat = tokens.next();
    # # rest of file contain new records
    # for token in tokens:
    #     item = {}
    #     for i, val in enumerate(token):
    #         if val:
    #             key = header[i]
    #             if headerFormat[i] == 'int':
    #                 val = int(val)
    #             item[key] = val
    #     print(item)
    #     table.put_item(Item=item)
    #
    #     time.sleep(1 / args.writeRate)  # to accomodate max write provisioned capacity for table
    #
    # #Parse contents of the file from csv to JSON
    #
    # item = {
    #     "fileName": {
    #         "S": file_name,
    #     },
    #     "fileContent": {
    #         "S": body
    #     },
    #     "fileSize": {
    #         "N": str(size)
    #     }
    # }
    #
    # print("test 123")
    #
    # return dynamodb.put_item(
    #     TableName=dynamodb_table_name,
    #     Item=item
    # )