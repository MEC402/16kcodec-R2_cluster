# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:02:03 2018

@author: IkerVazquezlopez
"""

import cv2
import os
import video
import sys


input_video = sys.argv[1]
dst_dir = sys.argv[2]

if not os.path.exists(dst_dir) or not os.path.isdir(dst_dir):
      os.makedirs(dst_dir)

#%% LOAD VIDEO

v, frame_count, frame_heigth, frame_width = video.load_video(input_video)



#%% WRITE INDIVIDUAL FRAMES INTO DESTINATION FOLDER

for f in range(0, frame_count):
      cv2.imwrite(dst_dir + "/" + str(f) + ".png", v[f] )
      
print("Decomposition finished!")
