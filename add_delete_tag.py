import json
import boto3



def add_tag(event, context):
    dynamodb = boto3.client('dynamodb')
    TABLE_NAME = 'TAG'
    data = json.loads(event['body']) 
    if event['queryStringparameters'] is not None:
        tag = data['queryStringParameters']['tag']
        url = data['queryStringParameters']['url']

        try:
            response = client.update_item(
                TABLE_NAME='TAG',
                Key={
                    'url': url
                },
                UpdateExpression='SET tags = list_append(tags, :t)',
                ExpressionAttributeValues={
                    ':t':[tag]
                },
                returnValue='UPDATE_NEW'
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
            


def delete_tag(event, context):
    dynamodb = boto3.client('dynamodb')
    TABLE_NAME = 'TAG'
    data = json.loads(event['body']) 
    if data['queryStringparameters'] is not None:
        url = data['queryStringParameters']['url']
        try:
            response = client.delete_item(
                TABLE_NAME='TAG',
                Key={
                    'url': url
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






