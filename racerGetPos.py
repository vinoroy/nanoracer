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

curTime = datetime.datetime.now().strftime('%H:%M:S')
print('start loading the model : '+ curTime)

# load the pretrained model from file
model = tf.keras.models.load_model('racerModel_210722.h5')

curTime = datetime.datetime.now().strftime('%H:%M:S')
print('finished loading the model : '+ curTime)

curTime = datetime.datetime.now().strftime('%H:%M:S')
print('start the camera : '+ curTime)

# create the camera object
camera = CSICamera(width=224, height=224, capture_width=1080, capture_height=720, capture_fps=30)


# read the camera and set to running. This will mean that we will only have to get the last value of the camera to get
# the latest frame
img = camera.read()
camera.running = True


# get the last value of the camera
img = camera.value


# rotate the image and convert to butes for the display widget
img = cv2.rotate(img, cv2.ROTATE_180)

curTime = datetime.datetime.now().strftime('%H:%M:S')
print('camera is ready : '+ curTime)

curTime = datetime.datetime.now().strftime('%H:%M:S')
print('prep data and make first prediction : '+ curTime)


# convert from integers to floats
X = img.astype('float32')

# normalize to range 0-1
X = X / 255.0

# need to perform a first prediction so the model is fast
XX = np.array([X])
y_pred = model.predict(XX)
y_pred[0][0]


curTime = datetime.datetime.now().strftime('%H:%M:S')
print('finished making the first prediction : '+ curTime)
print('-------')
print()
print()

lastTime = time.time() * 1000

# perform for 20 prames
for i in range(20):

    # get image value and rotate
    img = camera.value
    img = cv2.rotate(img, cv2.ROTATE_180)


    # convert image from integers to floats
    X = img.astype('float32')

    # normalize to range 0-1
    X = X / 255.0

    # insert in numpy array
    X = np.array([X])

    # make a prediction of the center line position
    y_pred = model.predict(X)
    result = y_pred[0][0]


    print('Frame No : ' + str(i) + 'Result : ' + str(result))

    #time.sleep(0.2)

    curTime = time.time() * 1000
    diffTime = curTime - lastTime
    print('line pred finished : '+ str(diffTime))

    lastTime = curTime
