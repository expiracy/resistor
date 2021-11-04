import glob
import os

import cv2 as cv
import numpy as np

# https://docs.opencv.org/master/d8/d4b/tutorial_py_knn_opencv.html

os.chdir("..")

directory = os.path.abspath(os.curdir)

for file_name in glob.glob(directory + '\\images\\croppedTrainingImages\\' + '*.jpg'):
    img = cv.imread(file_name)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    x = np.array(gray)

    train = x.reshape(-1, 400).astype(np.float32)
    test = x.reshape(-1, 400).astype(np.float32)


    k = np.arange(10)

    train_labels = np.repeat(k, 250)
    test_labels = train_labels.copy()

    knn = cv.ml.KNearest_create()
    knn.train(train, cv.ml.ROW_SAMPLE, train_labels)
    ret, result, neighbours, dist = knn.findNearest(test, k=5)
    # Now we check the accuracy of classification
    # For that, compare the result with test_labels and check which are wrong
    matches = result == test_labels
    correct = np.count_nonzero(matches)
    accuracy = correct*100.0/result.size
    print(accuracy)