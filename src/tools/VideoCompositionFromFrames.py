# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:24:15 2018

@author: IkerVazquezlopez
"""

import cv2
import os
import sys
from os.path import isfile, join
import video

def get_int(name):
      i = name.split('_')[1]
      return(int(i))

input_dir = sys.argv[1]

if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
      print("The input directory is not valid!")
      exit()

dst_video = input_dir + "output.mp4"


#%% GET THE FILENAMES IN THE DIRECTORY

filename_list = [f for f in os.listdir(input_dir) if isfile(join(input_dir, f))]
filename_list.sort(key=get_int)
#filename_list = sys.argv[2:]
print(filename_list)

#%% READ THE FILES

v = []
for f in range(0, len(filename_list)):
      img = cv2.imread(input_dir + filename_list[f])
      v.append(img)
      
      
#%% WRITE THE VIDEO

if len(v) > 0:
      video.write_video(dst_video, v)
else:
      print("There is no video write!")

