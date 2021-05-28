import json
import boto3

TABLE_NAME = 'IMAGE_URL'

def add_tag(event, context):
    db_resource = boto3.resource('dynamodb')
    table = db_resource.Table(TABLE_NAME) 
    data = json.loads(event['body'])

    if data[0]['url_list'] is not None:
        tags = data[1]['tags']
        url = data[0]['url_list']

        try:
            response = table.update_item(
                Key={
                    'url_list': url
                },
                UpdateExpression='SET tags = list_append(tags, :t)',
                ExpressionAttributeValues={
                    ':t':tags
                },
                ReturnValues='UPDATED_NEW'
            )
            
            print(response)
            return{
                'statusCode': 200
            }
        except Exception as e:
            print(e)
        return{
            'statusCode': 500
        }
            

def delete_item(event, context):
    db_resource = boto3.resource('dynamodb')
    table = db_resource.Table(TABLE_NAME) 
    data = json.loads(event['body'])

    if data[0]['url_list'] is not None:
        tags = data[1]['tags']
        url = data[0]['url_list']

        try:
            response = table.delete_item(
                Key={
                    'url_list' :url
                }
            )
            print(response)
            return{
                'statusCode': 200
            }
        except Exception as e:
            print(e)
        return{
            'statusCode': 500
    }



def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'POST':
        return add_tag(event, context)
    elif event['httpMethod'] == 'DELETE':
        return delete_item(event, context)
    else:
        return{
            'statusCode': 200
        }



""" {
  "body": "[{\"url_list\":\"url_test1\"},{\"tags\": [\"watermelon\",\"person\"]}]",
  "httpMethod": "POST"
} """