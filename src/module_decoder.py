# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 11:31:10 2018

@author: IkerVazquezlopez
"""

import sys
import pickle
import cv2
import gc


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
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
#out0 = cv2.VideoWriter("reconstructed0.avi", fourcc, 30.0, (int(background.shape[1]/2),int(background.shape[0]/2)), True)
#out1 = cv2.VideoWriter("reconstructed1.avi", fourcc, 30.0, (int(background.shape[1]/2),int(background.shape[0]/2)), True)
#out2 = cv2.VideoWriter("reconstructed2.avi", fourcc, 30.0, (int(background.shape[1]/2),int(background.shape[0]/2)), True)
#out3 = cv2.VideoWriter("reconstructed3.avi", fourcc, 30.0, (int(background.shape[1]/2),int(background.shape[0]/2)), True)
print(len(tracker.getFrames()))
for frame in tracker.getFrames():
    
    #background_frame = background.copy()
    background_frame = cv2.imread(sys.argv[2])
    #print(len(frame.getObjects()))
    for obj in frame.getObjects():
        if not str(obj.getID()) in loaded_videos:
            obj_cap = cv2.VideoCapture(obj_video_dir + str(obj.getID()) + ".avi")
            loaded_videos[str(obj.getID())] = obj_cap
        ret, v_obj_frame = loaded_videos[str(obj.getID())].read()
        #print(obj.getID(), ret)
        #print(v_obj_frame.shape)
        if not ret:
            continue
            
        x, y, _, _ = obj.getBbox()
        h, w, _ = v_obj_frame.shape
        
        if x+w > background_frame.shape[1]:
            x = x-(x+w-background_frame.shape[1])
        if y+h > background_frame.shape[0]:
            y = y-(y+h-background_frame.shape[0])
        
        background_frame[y:y+h, x:x+w] = v_obj_frame
    print(frame.getID())
    cv2.imwrite("../output/reconstructed_frames/" + str(frame.getID()) + ".png", background_frame)
    #out0.write(background_frame[0:int(background.shape[1]/2), 0:int(background.shape[0]/2)])
    #out1.write(background_frame[0:int(background.shape[1]/2), int(background.shape[0]/2):background.shape[0]])
    #out2.write(background_frame[int(background.shape[1]/2):background.shape[1], 0:int(background.shape[0]/2)])
    #out3.write(background_frame[int(background.shape[1]/2):background.shape[1], int(background.shape[0]/2):background.shape[0]])
    background_frame = None
    gc.collect()
#out0.release() 
#out1.release() 
#out2.release() 
#out3.release() 
        
