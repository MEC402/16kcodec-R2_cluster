# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:51:52 2018

@author: IkerVazquezlopez
"""

from tracker import Tracker
from object_manager import ObjectManager
import cv2
import video
import sys
import pickle
import gc
import os
from os import listdir
from os.path import isdir, isfile, join


if len(sys.argv) != 3:
    print(len(sys.argv))
    print("Usage: python module_generate_obj_videos.py src_dir_path trackerpath")
    raise Exception("GenerateObjVideos: main --> Input arguments != 3.") 
    
    
src_dir_path = sys.argv[1]
tracker_path = sys.argv[2]
tmp_dir = tracker_path[:-11] # remove the file from tracker_path to get the tmp dir

# Load the tracker
file = open(tracker_path, 'rb')
tracker = pickle.load(file)
file.close()


# Add all the objects to the object manager
obj_manager = ObjectManager()
for f in range(0, len(tracker.getFrames())):
      frame = tracker.getFrame(f)
      obj_manager.add_frame(frame.getObjects(),f)

# Compute the maximum bbox for each of the objects
obj_manager.compute_obj_max_bboxes()

# Get the frames for each of the objects and write the videos
max_bboxes = obj_manager.getMaxBboxObjects()
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
for f in range(0, len(tracker.getFrames())):
      frame = tracker.getFrame(f)
      image = cv2.imread(src_dir_path + "anim_{id}_4k.png".format(id=frame.getKey()))
      frame_heigth, frame_width, _ = image.shape
      for obj in frame.getObjects():
            x, y, w, h = obj.getBbox()
            video_bbox_w, video_bbox_h = max_bboxes[obj.getID()]
            if x + video_bbox_w >= frame_width:
                  x = x - (x + video_bbox_w - frame_width)
            if y + video_bbox_h >= frame_heigth:
                  y = y - (y + video_bbox_h - frame_heigth)
            obj_dir = "{}object_frames/{}/".format(tmp_dir, obj.getID())
            if not os.path.isdir(obj_dir):
                  os.mkdir(obj_dir)
            cv2.imwrite(obj_dir + str(f).zfill(6) + ".png", image[y:(y+video_bbox_h), x:(x+video_bbox_w)])
      
      obj_manager.add_frame(frame.getObjects(),f)
        

# Check that the resulting filenames for objects start at 000000.png (for FFMPEG library)
obj_dir = "{}object_frames/".format(tmp_dir)
directories = [f for f in listdir(obj_dir) if isdir(join(obj_dir, f))]
for d in directories:
    filenames = [f for f in listdir(obj_dir + d) if isfile(join(obj_dir + d, f))]
    init_frame = int(filenames[0].split('.')[0])
    for f in filenames:
        curr_frame = int(f.split('.')[0])
        curr_frame = curr_frame - init_frame
        os.rename(obj_dir + d + "/" + f, obj_dir + d + "/" + str(curr_frame).zfill(6) + ".png")    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
