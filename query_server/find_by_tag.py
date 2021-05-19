import json
import boto3
import base64

dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'TAG'


def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'POST':
        data = json.loads(event['body'])   # request have body
        tags_encode = data['tags']  # user's tags request

        tags = base64.b64decode(tags_encode)  # list of tags
        tags = list(set(tags))   # remove repeated tags

        url_set = {}

        # assume we have two tables, one is url table, one is tags table
        for tag in tags:
            response = dynamodb.query(
                TableName=TABLE_NAME,
                KeyConditionExpression='tag_title = :tag_title',
                ExpressionAttributeValues={
                    ':tag_title': {'S': tag}
                }
            )
            url_set = url_set & set(response)

        url_list = list(url_set)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "links": url_list
            })
        }