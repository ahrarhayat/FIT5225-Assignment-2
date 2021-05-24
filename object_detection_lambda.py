import json
import base64
import numpy as np
import sys
import time
import os
import cv2
from PIL import Image
import io
import boto3


# construct the argument parse and parse the arguments
confthres = 0.5
nmsthres = 0.1
s3 = boto3.client('s3')

#def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on
   # lpath = os.path.sep.join([yolo_path, labels_path])

  #  print(yolo_path)
  #  LABELS = open(lpath).read().strip().split("\n")
  #  return LABELS


#def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
 #   weightsPath = os.path.sep.join([yolo_path, weights_path])
 #   return weightsPath


#def get_config(config_path):
  #  configPath = os.path.sep.join([yolo_path, config_path])
  #  return configPath


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

    # TODO Prepare the output as required to the assignment specification(DONE)
    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        # create an array of the results
        result = []
        #loop over the objects and put them in an array and return the result
        for i in idxs.flatten():
            result.append({"label": LABELS[classIDs[i]], "accuracy": confidences[i],
                           "rectangle": {"height": boxes[i][0], "left": boxes[i][1], "top": boxes[i][2],
                                         "width": boxes[i][3]}})
        return result
        
## argument
#if len(sys.argv) != 2:
    #raise ValueError("Argument list is wrong. Please use the following format:  {} {}".
          #           format("python object_detection.py", "<yolo_config_folder>"))
          
#This path must be changed to s3 reference
bucket = 'library-bucket-ahrar'
key1 = 'coco.names'
key2 = 'yolov3-tiny.cfg'
key3 = 'yolov3-tiny.weights'
s3_resource1 = boto3.resource('s3')
s3_bucket = s3_resource1.Bucket(bucket)
s3_obj1 = s3_bucket.Object(key=key1)
s3_resource2 = boto3.resource('s3')
s3_bucket = s3_resource2.Bucket(bucket)
s3_obj2 = s3_bucket.Object(key=key2)
s3_resource3 = boto3.resource('s3')
s3_bucket = s3_resource3.Bucket(bucket)
s3_obj3 = s3_bucket.Object(key=key3)
        


#print(response)
#yolo_path = str(response)

## Yolov3-tiny versrion
#labelsPath = "coco.names"
#cfgpath = "yolov3-tiny.cfg"
#wpath = "yolov3-tiny.weights"


def lambda_handler(event, context):
    
    print('Lamda handler started')
    
    
    # read image which is uplaoded to bucker
    
    
    # read yolo files from bucket 
    #boto to get file from bucket
    
    labels = s3_obj1
    cfg = s3_obj2
    weights = s3_obj3
    
    # do obejct detection
    
    
    # insert in db
    
    # TODO implement
    #image from the s3 bucket
    #img = Image.open(io.BytesIO(image_data))
        # now that the image is extracted, use the same methods as before and use the methods to get the objects
        # img = cv2.imread(filename)
    #npimg = np.array(img)
    #image = npimg.copy()
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # load the neural net.  Should be local to this method as its multi-threaded endpoint
    #nets = load_model(CFG, Weights)
    #result = do_prediction(image, nets, Lables)
    
