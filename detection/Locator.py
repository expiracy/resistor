from imageai.Detection.Custom import CustomObjectDetection

import tensorflow

class Locator:

    def train(self):
        detector = CustomObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath("hololens-ex-60--loss-2.76.h5")
        detector.setJsonPath("detection_config.json")
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image="holo3.jpg", output_image_path="holo3-detected.jpg")
        for detection in detections:
            print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])


#locator = Locator()
#locator.train()
