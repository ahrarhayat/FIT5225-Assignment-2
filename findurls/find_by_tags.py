import json
import boto3
import base64

TABLE_NAME = 'IMAGE_URL'


def get_urls(tags, items):
    url_list = []
    for item in items:
        if set(item['tags']) & set(tags) == set(tags):
            url_list.append(item['url_list'])
    return url_list


def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'POST':
        data = json.loads(event['body'])  # request have body

        tags_encode = data['tags']  # user's tags request

        # tags = base64.b64decode(tags_encode)  # list of tags. not sure will have encoded message or not
        urls = []
        tags = set(tags_encode)  # remove repeated tags
        try:
            if len(tags) != 0:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table(TABLE_NAME)
                response = table.scan()
                items = response['Items']
                urls = get_urls(tags, items)

        except Exception:
            print("Getting items failed")

        return {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({
                "links": urls
            })
        }
