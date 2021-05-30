import json
import boto3


TABLE_NAME = 'IMAGE_URL'

            
def delete_item(event, context):
    s3_resource = boto3.resource('s3')
    db_resource = boto3.resource('dynamodb')
    table = db_resource.Table(TABLE_NAME) 
    s3_bucket = "s3-image-storing-bucket-fit5225"
    
    data = json.loads(event['body'])

    if data['url'] is not None:

        url = data['url']
        key = url.split('/')[-1]
        #return key
        #key = urlparse(url).path
        s3_resource.Object('s3-image-storing-bucket-fit5225', key).delete()
        
        try:
            response = table.delete_item(
                Key={
                    'url_list' :url
                }
            )
            print(response)
            return{
                'statusCode': 200,
            "headers": {
                'Access-Control-Allow-Origin': '*'
            }
            }
        except Exception as e:
            print(e)
        return{
            'statusCode': 500,
            "headers": {
                'Access-Control-Allow-Origin': '*'
            }
    }


def lambda_handler(event, context):
    
    if event['httpMethod'] == 'POST':
        return delete_item(event, context)
    else:
        return{
            'statusCode': 200,
            "headers": {
                'Access-Control-Allow-Origin': '*'
            }
        }

