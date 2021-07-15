from cmd import Cmd
from jetcam.csi_camera import CSICamera
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Racer(Cmd):

    # session variables
    sessionInst = None
    
    camera = CSICamera(width=224, height=224, capture_width=1080, capture_height=720, capture_fps=30)
    
    imageLst = []
    imageArray = None
    

    def do_bye(self, inp):
        '''exit the application.'''

        print("Bye")
        print('')
        return True


    def do_tp(self,t):
        '''take picture and insert into list '''
        
        image = self.camera.read()

        img_rotate_180 = cv2.rotate(image, cv2.ROTATE_180)
        
        self.imageLst.append(img_rotate_180)
        
    
        
    
    
    def do_conv(self,t):
        '''convert list of images into numpy array of images '''
        
        train = np.array(self.imageLst,dtype='float32')
        
        print(train.shape)
    
    
    
    def do_prt(self,t):
        '''print list '''
        
        print(len(self.imageLst))
        
    
    def do_save(self,t):
        '''save numpy array '''
        
        print(len(self.imageLst))
        
    
        
Racer().cmdloop()


