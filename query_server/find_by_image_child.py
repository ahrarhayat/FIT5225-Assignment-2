import json
import os
from datetime import time

import boto3
import base64
import numpy as np
import cv2

# construct the argument parse and parse the arguments
confthres = 0.3
nmsthres = 0.1


def get_labels(labels_path):
    lpath = os.path.sep.join([yolo_path, labels_path])

    print(yolo_path)
    LABELS = open(lpath).read().strip().split("\n")
    return LABELS


def get_weights(weights_path):
    weightsPath = os.path.sep.join([yolo_path, weights_path])
    return weightsPath


def get_config(config_path):
    configPath = os.path.sep.join([yolo_path, config_path])
    return configPath


def load_model(configpath, weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net


def detect_object(image, net, LABELS):
    (H, W) = image.shape[:2]
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > confthres:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    detected_objects = []
    if len(idxs) > 0:
        for i in idxs.flatten():
            detected_object = {}

            rectangle = {
                'height': boxes[i][3],
                'left': boxes[i][0],
                'top': boxes[i][1],
                'width': boxes[i][2]
            }

            detected_object = {
                'label': LABELS[classIDs[i]],
                'accuracy': confidences[i],
                'rectangle': rectangle
            }

            detected_objects.append(detected_object)
    return detected_objects


def get_urls(response):
    url_list = []
    for item in response['Items']:
        url_list.append(item['url']['S'])
    return url_list


# This path must be changed to s3 reference
yolo_path = 'yolo_tiny_configs'

labelsPath = "coco.names"
cfgpath = "yolov3-tiny.cfg"
wpath = "yolov3-tiny.weights"

Lables = get_labels(labelsPath)
CFG = get_config(cfgpath)
Weights = get_weights(wpath)

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

        nets = load_model(CFG, Weights)  # yolo model
        tags = detect_object(image, nets, Lables)  # invoke detect object function?

        tags = list(set(tags))
        url_set = {}

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
