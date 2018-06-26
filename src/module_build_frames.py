# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 10:14:45 2018

@author: IkerVazquezlopez
"""

import sys
import pickle
import cv2
import numpy as np

target_h = 2160
target_w = 4096
target_shape = (target_h, target_w, 3)




#%% MAIN METHOD


if len(sys.argv) != 3:
    print(len(sys.argv))
    print("Usage: python module_build_frames.py tracker_path obj_video_dir")
    raise Exception("Frame builder: main --> Input arguments != 3.") 
    
    
tracker_path = sys.argv[1]
obj_video_dir = sys.argv[2]

f = open(tracker_path, 'rb')
tracker = pickle.load(f)
f.close()



loaded_videos = {}

# Variables to get track of organization of the frame
curr_x = 0
curr_y = 0
max_y = 0   # This will change based on the height of the objects to jump to the next line



for frame in tracker.getFrames():
    target_frame = np.zeros(target_shape, dtype = np.uint8)
    objects = {}
    for obj in frame.getObjects():
        if not str(obj.getID()) in loaded_videos:
            obj_cap = cv2.VideoCapture(obj_video_dir + str(obj.getID()) + ".avi")
            loaded_videos[str(obj.getID())] = obj_cap
        ret, v_obj_frame = loaded_videos[str(obj.getID())].read()
       
        if not ret:
            continue
        h, w, _ = v_obj_frame.shape
        if curr_y + h > target_h and curr_x + w > target_w: # No more room, report to the user
            raise Exception("Frame builder: not enough room for objects in target frame!")
        if curr_x + w > target_w:   # Jump to the next line if necessary
            curr_y = max_y
            curr_x = 0
        if curr_y + h > max_y:  # Update max_y
            max_y = curr_y + h
        
        objects[str(obj.getID())] = (curr_y, curr_x, h, w)  # Store obj's coords at the target frame
        target_frame[curr_y:curr_y+h, curr_x:curr_x+w] = v_obj_frame    # Add the object to the target frame
        
        curr_x = curr_x + w
        
        
        
    print(frame.getID())
    cv2.imwrite("frame_builder/" + str(frame.getID()) + ".png", target_frame)
    
    f = open("frame_builder/" + str(frame.getID()) + ".pkl", 'wb')
    pickle.dump(objects, f)
    f.close()
    

        