from lineDetect import *
import time

myDetect = lineDetector('racerModel_210722.h5')


for i in range(20):


    print(myDetect.getPos())

    time.sleep(1)

