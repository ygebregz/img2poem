
"""
This class is responsible for analyzing an image and return 
a list of objects that are present in the image.

TODO: Add documentations all throughout 
"""
import cv2
import numpy as np
import urllib.request
import os

YOLO_WEIGHTS_URL = "https://pjreddie.com/media/files/yolov3.weights"


class ImageObjectDetection:

    def __init__(self, recognition_confidence: int = 0.5) -> None:
        print("Loading imga detecion model")
        self.net = cv2.dnn.readNet(
            self.download_yolo_weights(), "model/yolo/yolov3.cfg")
        print("Image detecion model loaded!")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1]
                              for i in self.net.getUnconnectedOutLayers()]
        self.recognition_confidence = recognition_confidence
        # Loading the COCO class labels
        with open("model/yolo/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def download_yolo_weights(self, file_path: str = "model/yolo/yolov3.weights") -> bool:
        if os.path.exists(file_path):
            print("weights already exist")
            return file_path
        else:
            print("Downloading weights")
            urllib.request.urlretrieve(YOLO_WEIGHTS_URL, file_path)
            return file_path

    def get_img_output_layers(self, image_path: str = "data/images/dog.jpg"):
        self.image = cv2.imread(image_path)
        blob = cv2.dnn.blobFromImage(
            self.image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        return self.net.forward(self.output_layers)

    def get_label(self, img_output_layer):
        print("Detecting objects")
        class_ids = []
        for out in img_output_layer:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.recognition_confidence:
                    # Object detected
                    class_ids.append(class_id)
        labels = set()
        for i in range(len(class_ids)):
            label = self.classes[class_ids[i]]
            labels.add(label)
        return list(labels)
