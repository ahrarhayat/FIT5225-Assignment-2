import json
import boto3
import base64

dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'TAG'


def get_urls(response):
    url_list = []
    for item in response['Items']:
        url_list.append(item['url']['S'])
    return url_list


def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'POST':
        data = json.loads(event['body'])  # request have body
        tags_encode = data['tags']  # user's tags request

        # tags = base64.b64decode(tags_encode)  # list of tags

        tags = list(set(tags_encode))  # remove repeated tags

        url_set = set()
        i = 0
        tags_num = len(tags)

        # assume we have two tables, one is url table, one is tags table
        while i < tags_num:
            response = dynamodb.query(
                TableName=TABLE_NAME,
                KeyConditionExpression='tag_title = :tag_title',
                ExpressionAttributeValues={
                    ':tag_title': {'S': tags[i]}
                }
            )

            if i == 0:
                url_set = set(get_urls(response))
            else:
                url_set = url_set & set(get_urls(response))
            i += 1

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "links": list(url_set)
            })
        }


'''
{
  "body": "{\"tags\": [\"cat\", \"person\"]}",
  "httpMethod": "POST"
}
'''
