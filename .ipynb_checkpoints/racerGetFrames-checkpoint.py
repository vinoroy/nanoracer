import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

from jetcam.csi_camera import CSICamera

import time


# create the camera object
camera = CSICamera(width=224, height=224, capture_width=1080, capture_height=720, capture_fps=30)


# variable to store the captured images and the current image
imageList = []
currentImg = None


# read the camera and set to running. This will mean that we will only have to get the last value of the camera to get
# the latest frame
img = camera.read()
camera.running = True


print('Start taking frames')

# perform for 300 images
for i in range(400):

    # get image from the camera
    img = camera.value
    img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)

    # rotate the image
    currentImg = img_rotate_180

    # add the image to list of captured images
    imageList.append(currentImg)

    time.sleep(0.1)
    
    print('Frame number : ' + str(i))
    
    
images = np.array(imageList)
print('Exporting the frames')
                
np.save('./trackImagesTemp.npy', images)
print('Finished exporting the frames')
