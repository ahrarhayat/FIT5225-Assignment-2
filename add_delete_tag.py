import json
import boto3

TABLE_NAME = 'a3test'

def add_tag(event, context):
    db_resource = boto3.resource('dynamodb')
    table = db_resource.Table(TABLE_NAME) 
    data = json.loads(event['body'])

    if data[0]['url'] is not None:
        tags = data[1]['tags']
        url = data[0]['url']

        try:
            response = table.update_item(
                Key={
                    'url': url
                },
                UpdateExpression='SET tags = list_append(tags, :t)',
                ExpressionAttributeValues={
                    ':t':[tags]
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

    if data[0]['url'] is not None:
        tags = data[1]['tags']
        url = data[0]['url']

        try:
            response = table.delete_item(
                Key={
                    'url' :url
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
    if event['httpMethod'] == 'PUT':
        return add_tag(event, context)
    elif event['httpMethod'] == 'DELETE':
        return delete_item(event, context)
    else:
        return{
            'statusCode': 200
        }


""" {
  "body": "[{\"url\":\"url3\"},{\"tags\": [\"watermelon\",\"person\"]}]",
  "httpMethod": "PUT"
} """