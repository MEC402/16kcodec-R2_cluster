# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 09:21:49 2018

@author: IkerVazquezlopez
"""

import cv2
import numpy as np
import sys

#input_dir = "../videos/output/"
#output_dir = "../videos/output_diff/"
input_dir = "../video_source/"
output_dir = "../tmp/differences/"



"""
      Rreturns the detected movement in each frame of the video. If a pixel
      has a value of 0, there is no movement. Otherwise, if the pixel has a
      value >0, a movement was detected.
      
      @param frame0, current video frame.
      @param frame1, next video frame.
      @param mode, the method tu use.
      @param remaining arguments, specific arguments for each of the methods.
"""
def detect_movement(frame0name, frame1name, mode="frame_differences", n=None, background_img=None):
    
    frame0 = cv2.imread(input_dir + frame0name)
    frame1 = cv2.imread(input_dir + frame1name)
    
    
    if mode == "frame_differences":
        return __frame_difference(frame0, frame1)
      #if mode == "background_difference":
      #      return __background_difference(v, background_img)
      #if mode == "optical_flow":
      #      return __optical_flow(v)







#%% FRAME DIFFERENCES

"""
      Returns a video of the frame differences. By default the frame difference
      is computed using the previous frame (n=1). If the @param n is defined,
      the n previous frames are considered to compute the difference.
      
      @param frame0, current video frame.
      @param frame1, next video frame.
"""
def __frame_difference(frame0, frame1):
      
    if frame0 is None or frame1 is None:
        raise ValueError("MovementDetection:__frame_difference(frame0,frame1) --> Error reading the frames!")
      
    return cv2.absdiff(frame0, frame1)
           


#%% BACKGROUND DIFFERENCE

"""
      Returns a video of the frame differences against a background image. 
      Each of the video frames are substracted to the background and the 
      resulting image is saved as a frame in the video.
      
      @param v, the input video
      @param background, background image of the video.
"""
#def __background_difference(v, background=None):
#      
#      if len(v) == 0:
#            raise ValueError("MovementDetection:__background_differences(v,background) --> Empty video!")
#      
#      if background == None:
#            raise ValueError("MovementDetection:__background_differences(v,background) --> @param background == None")
#      
#      return [cv2.absdiff(v[f], background) for f in tqdm(range(0,len(v)))]
#
#
#




#%% OPTICAL FLOW

#def __optical_flow(v):
#      opt_flow = []
#      for i in tqdm(range(1,len(v))):
#            prev = cv2.cvtColor(v[i-1], cv2.COLOR_BGR2GRAY)
#            prev = cv2.GaussianBlur(prev, (7,7), 5.0)
#            curr = cv2.cvtColor(v[i], cv2.COLOR_BGR2GRAY)
#            curr = cv2.GaussianBlur(curr, (7,7), 5.0)
#            
#            hsv = np.zeros((prev.shape[0], prev.shape[1], 3), dtype=np.float32)
#            flow = cv2.calcOpticalFlowFarneback(prev,curr, None, 0.5, 3, 15 , 3, 5, 1.2, cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
#            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
#                
#            hsv[...,1] = 255
#            hsv[...,0] = ang*180/np.pi/2
#            hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
#            opt_flow.append(hsv)
#                
#      return opt_flow


#%% MAIN METHOD


if len(sys.argv) != 3:
    print(len(sys.argv))
    print("Usage: python module_movement_detection.py filename0 filename1")
    raise Exception("MovementDetection: main --> Input arguments != 3.") 
    
filename0 = sys.argv[1]
filename1 = sys.argv[2]
diff_img = detect_movement(filename0, filename1, mode="frame_differences")


tokens = filename0.split('.')
output_filename = tokens[0] + "_diff." + tokens[1]
output_filename = output_dir + output_filename

cv2.imwrite(output_filename, diff_img)
    
    
    





            
