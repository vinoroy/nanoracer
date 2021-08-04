import numpy as np

#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

import random

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import *

import datetime
import time

from jetcam.csi_camera import CSICamera

import cv2

import time


class lineDetector():

    def __init__(self,modelFile):

        self.modelFile = modelFile

        # load the pretrained model from file
        self.model = tf.keras.models.load_model(self.modelFile)


        # create the camera object
        self.camera = CSICamera(width=224, height=224, capture_width=1080, capture_height=720, capture_fps=30)


        # read the camera and set to running. This will mean that we will only have to get the last value of the camera to get
        # the latest frame
        img = self.camera.read()
        self.camera.running = True


        # get the last value of the camera
        img = self.camera.value


        # rotate the image and convert to butes for the display widget
        img = cv2.rotate(img, cv2.ROTATE_180)


        # convert from integers to floats
        X = img.astype('float32')

        # normalize to range 0-1
        X = X / 255.0

        # need to perform a first prediction so the model is fast
        XX = np.array([X])
        y_pred = self.model.predict(XX)
        y_pred[0][0]

        print()
        print('-------')
        print('Finished initalizing the line detector')
        print('-------')
        print()
        print()


    def getPos(self):

        # get image value and rotate
        img = self.camera.value
        img = cv2.rotate(img, cv2.ROTATE_180)


        # convert image from integers to floats
        X = img.astype('float32')

        # normalize to range 0-1
        X = X / 255.0

        # insert in numpy array
        X = np.array([X])

        # make a prediction of the center line position
        y_pred = self.model.predict(X)
        result = y_pred[0][0]


        print('Result : ' + str(result))

        return result


if __name__=='__main__' :

    print('ok')

    myDetect = lineDetector('racerModel_210722.h5')

    print(myDetect.getPos())
