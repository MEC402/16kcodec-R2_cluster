# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 11:31:10 2018

@author: IkerVazquezlopez
"""

import sys
import pickle
import cv2


def obj_in_list(obj, loaded_list):
    for e in loaded_list:
        if obj.getID() == e[0]:
            return True
    return False



#%% MAIN METHOD


if len(sys.argv) != 4:
    print(len(sys.argv))
    print("Usage: python module_decoder.py tracker_path background_path obj_video_dir")
    raise Exception("Decoder: main --> Input arguments != 4.") 
    
    
tracker_path = sys.argv[1]
obj_video_dir = sys.argv[3]

f = open(tracker_path, 'rb')
tracker = pickle.load(f)
f.close()



loaded_videos = {}

background = cv2.imread(sys.argv[2])
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
out = cv2.VideoWriter("reconstructed.mp4", fourcc, 20.0, (background.shape[1],background.shape[0]), True)

for frame in tracker.getFrames():
    background_frame = background.copy()
    #print(len(frame.getObjects()))
    for obj in frame.getObjects():
        if not str(obj.getID()) in loaded_videos:
            obj_cap = cv2.VideoCapture(obj_video_dir + str(obj.getID()) + ".avi")
            loaded_videos[str(obj.getID())] = obj_cap
        ret, v_obj_frame = loaded_videos[str(obj.getID())].read()
        if not ret:
            continue
        x, y, _, _ = obj.getBbox()
        h, w, _ = v_obj_frame.shape
        background_frame[y:y+h, x:x+w] = v_obj_frame
    #cv2.imwrite("reconstruction/" + str(frame.getID()) + ".png", background_frame)
    out.write(background_frame)
            
        
