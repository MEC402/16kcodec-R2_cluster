# -*- coding: utf-8 -*-
"""
Created on Mon May 21 11:11:17 2018

@author: IkerVazquezlopez
"""

from tracker import Tracker
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import sys

import pickle

import cv2

def point_distance(A, B):
    return ( (A[0]-B[0])**2 + (A[1]-B[1])**2 ) **0.5

def track_objects(prev_objects, frame_objects, threshold, tracker):
        # Initialize helper vairables
        return_objects = []
        # Iterate through previous objects
        for o in range(0,len(prev_objects)):
                min_distance = 99999
                min_object = None
                o_bbox = prev_objects[o].getBbox()
                # Find the closest match in the current frame within a threshold
                for i in range(0,len(frame_objects)):
                        curr_object = frame_objects[i]
                        i_bbox = frame_objects[i].getBbox()
                        i_c = ((i_bbox[0]+i_bbox[2])/2, (i_bbox[1]+i_bbox[3])/2)
                        o_c = ((o_bbox[0]+o_bbox[2])/2, (o_bbox[1]+o_bbox[3])/2)
                        d = point_distance(o_c, i_c)
                        if d < min_distance and d < threshold:
                                min_distance = d
                                min_object = curr_object
                if min_object is not None:
                        min_object.setID(prev_objects[o].getID())
                        min_object.setMask(prev_objects[o].getMask())
                        return_objects.append(min_object)
        # Remove found objects
        for i in range(0, len(return_objects)):
                for o in frame_objects:
                        if return_objects[i].getID() == o.getID():
                                frame_objects.remove(o)
                                break
        # Mark the new objects
        for i in range(0, len(frame_objects)):
                obj = frame_objects[i]; obj.setID(tracker.getLastObjectID())
                return_objects.append(obj)
                tracker.addOneLastObjectID()
        return return_objects
    
#%% MAIN METHOD

if len(sys.argv) != 2:
    print(len(sys.argv))
    print("Usage: python module_find_bboxes.py directory")
    raise Exception("FindBboxes: main --> Input arguments != 2.") 
    
dir_path = sys.argv[1]


filenames = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

groups = defaultdict(list)
for f in filenames:
    frame_id = f.split("_")[1]
    groups[frame_id].append(f)
    
n_frames = len(groups)

tracker = Tracker()
tracker.fillFrames(n_frames)

# Generate bounding boxes ------------------------------------------
for f in range(0, n_frames):
    frame = tracker.getFrame(f)
    for c in range(0,len(groups[f])):
        mask = cv2.imread(groups[f][c])
        contours = cv2.findContours(mask, 2, 2)[1][0]
        frame.appendObject(cv2.boundingRect(contours))
        
        
# Assign an ID to each object-bbox -----------------------------------
f_o_rect_id = []
id_frames = []
tracked = []
prev_objects = []
OBJECT_THRESHOLD = 50 # maximum distance to determine if it is the same object (after movemnt)
for f in range(0, len(tracker.getFrames())):
    frame = tracker.getFrame(f)
    objects = frame.getObjects()
    if len(objects) > 0:
          prev_objects = track_objects(prev_objects, objects, OBJECT_THRESHOLD, tracker)
          frame.setObjects(prev_objects)
        
        
        
        
# Write the tracker object
file = open(dir_path + "tracker.pkl", 'w')
pickle.dump(tracker, file)
file.close()
