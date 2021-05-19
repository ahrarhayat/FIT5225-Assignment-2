import json
import boto3
import base64

import numpy as np
import cv2

dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'TAG'


def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'POST':
        data = json.loads(event['body'])
        image_encode = data['image']
        image = base64.b64decode(image_encode)  # ??

        # https://stackoverflow.com/questions/17170752/python-opencv-load-image-from-byte-string
        image_np = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(image_np, 1)
        np_img = np.array(img)
        image = np_img.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        '''
        nets = load_model(CFG, Weights)  # yolo model
        tags = detect_object(image, nets, Lables)  # invoke detect object function?
        '''
        tags = []  # default, no use
        tags = list(set(tags))
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