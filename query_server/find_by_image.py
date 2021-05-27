import json
import base64
import numpy as np
import time
import cv2
import boto3
import os

# construct the argument parse and parse the arguments
confthres = 0.5
nmsthres = 0.1
TABLE_NAME = 'TAG'


def get_key(folder_name, key_name):
    return os.path.join(folder_name, key_name)


def get_urls(tags, items):
    url_list = []
    for item in items:
        if set(item['tags']) & set(tags) == set(tags):
            url_list.append(item['url'])
    return url_list


def load_model(configpath, weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net


def do_prediction(image, net, LABELS):
    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    # print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # ensure at least one detection exists
    detected_tags = []
    if len(idxs) > 0:
        for i in idxs.flatten():
            detected_tags.append(LABELS[classIDs[i]])

    return detected_tags


dynamodb_resource = boto3.resource('dynamodb')

# This path must be changed to s3 reference
bucket = 'tagtag-bucket'

folder = 'yolo_tiny_configs'
key1 = 'coco.names'
key2 = 'yolov3-tiny.cfg'
key3 = 'yolov3-tiny.weights'

s3_resource = boto3.resource('s3')
s3_obj1 = s3_resource.Object(bucket, key=get_key(folder, key1))
s3_obj2 = s3_resource.Object(bucket, key=get_key(folder, key2))
s3_obj3 = s3_resource.Object(bucket, key=get_key(folder, key3))


def lambda_handler(event, context):
    print('Lamda handler started')

    data = json.loads(event['body'])
    image_encode = data['image']
    image_decode = base64.b64decode(image_encode)  # ??

    labels = s3_obj1.get().get('Body').read()
    labels = str(labels)
    labels = labels[2:]
    labels.replace('"', '')
    labels = labels.split("\\n")

    cfg = s3_obj2.get().get('Body').read()
    weights = s3_obj3.get().get('Body').read()

    # https://stackoverflow.com/questions/17170752/python-opencv-load-image-from-byte-string
    image_np = np.frombuffer(image_decode, np.uint8)
    img = cv2.imdecode(image_np, 1)

    np_img = np.array(img)
    image = np_img.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    nets = load_model(cfg, weights)  # yolo model
    detected_tags = do_prediction(image, nets, labels)  # invoke detect object function?

    # do obejct detection
    urls = []
    tags = set(detected_tags)  # remove repeated tags

    try:
        if len(tags) != 0:
            table = dynamodb_resource.Table(TABLE_NAME)
            response = table.scan()
            items = response['Items']
            urls = get_urls(tags, items)

    except Exception:
        print("Getting items failed")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "links": urls
        })
    }
