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


if len(sys.argv) != 4:
    print(len(sys.argv))
    print("Usage: python module_generate_obj_videos.py src_dir_path trackerpath output_dir_path")
    raise Exception("GenerateObjVideos: main --> Input arguments != 4.") 
    
    
src_dir_path = sys.argv[1]
tracker_path = sys.argv[2]
output_dir = sys.argv[3]
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
      print(f)
      frame = tracker.getFrame(f)
      print(src_dir_path)
      image = cv2.imread(src_dir_path + "anim_{id}_4k.png".format(id=frame.getKey()))
      frame_heigth, frame_width, _ = image.shape
      for obj in frame.getObjects():
            x, y, w, h = obj.getBbox()
            video_bbox_w, video_bbox_h = max_bboxes[obj.getID()]
            if x + video_bbox_w >= frame_width:
                  x = x - (x + video_bbox_w - frame_width)
            if y + video_bbox_h >= frame_heigth:
                  y = y - (y + video_bbox_h - frame_heigth)
            #obj.setImage(image[y:(y+video_bbox_h), x:(x+video_bbox_w)])
            cv2.imwrite(tmp_dir + "object_frames/" + str(f) + "_" + str(obj.getID()) + ".png", image[y:(y+video_bbox_h), x:(x+video_bbox_w)])
            #obj.setMask(frame.getMask()[y:(y+video_bbox_h), x:(x+video_bbox_w)])
      
      obj_manager.add_frame(frame.getObjects(),f)

      
#obj_manager.write_individual_videos("output/objects/")
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
for obj_id in range(0, 1200):
    out = None
    print(obj_id)
    for f in range(0, len(tracker.getFrames())): 
        print(tmp_dir + "object_frames/" + str(f) + "_" + str(obj_id) + ".png")
        frame = cv2.imread(tmp_dir + "object_frames/" + str(f) + "_" + str(obj_id) + ".png")
        if frame is None:
            continue
        if out is None:
            out = cv2.VideoWriter(output_dir + "objects/" + str(obj_id) + ".avi", fourcc, 20.0, (frame.shape[1],frame.shape[0]), True)
        out.write(frame)
    if not out is None:
        out.release()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
