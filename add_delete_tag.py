import json
import boto3



def add_tag(event, context):
    db_resource = boto3.resouce('dynamodb')
    table = db_resource.Table('xxx') # not sure the table name
    if event['queryStringparameters'] is not None:
        etag = event['queryStringParameters']['etags']
        tag = event['queryStringParameters']['tag']
    # user = event['requestContext']['identity']['user']
    # print(user)
    # user = 'AWS:' + user
    # etags = []
        try:
            response = table.update_item(
                Key={
                    'etag': etag
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
    db_resource = boto3.resouce('dynamodb')
    table = db_resource.Table('xxx') # not sure the table name
    if event['queryStringparameters'] is not None:
        etag = event['queryStringParameters']['etags']
        try:
            response = table.delete_item(
                Key={
                    'etag': etag
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






