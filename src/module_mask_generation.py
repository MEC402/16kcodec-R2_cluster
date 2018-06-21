# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:20:40 2018

@author: IkerVazquezlopez
"""

import sys
import os
import cv2
import numpy as np

# General params
input_dir = "differences/"
output_dir = "masks/"

# Candidate pixel classification params
epsilon = 20
kernel1 = np.ones((3,3), np.uint8)
kernel2 = np.ones((7,7), np.uint8)
dilate_it = 10

# Connected Components params
connectivity = 8

#%% CANDIDATE PIXEL CLASSIFICATION

def generate_blobs(frame):
    f_c = cv2.threshold(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), epsilon, 255, cv2.THRESH_BINARY)[1]
    
    f_c = cv2.dilate(f_c, kernel1, iterations = dilate_it)
    f_c = cv2.morphologyEx(f_c, cv2.MORPH_CLOSE, kernel2)
    f_c = cv2.erode(f_c, kernel1, iterations = dilate_it)
    f_c = cv2.dilate(f_c, kernel1, iterations = dilate_it) 
    f_c = cv2.morphologyEx(f_c, cv2.MORPH_OPEN, kernel2)
    f_c = cv2.morphologyEx(f_c, cv2.MORPH_CLOSE, kernel2)
    
    return f_c

#%% COMPUTE CONNECTED COMPONENTS
    
def CCL(binary):
    ret, labels = cv2.connectedComponents(binary, connectivity)

    return labels

#%% GENERATE MASKS

def generate_masks(labels):
    f_o = [np.uint8(labels == i)*255 for i in range(1, np.max(labels)+1)]
    
    return f_o


#%% MAIN METHOD


if len(sys.argv) != 2:
    print(len(sys.argv))
    print("Usage: python module_mask_generation.py filename")
    raise Exception("BlobGeneration: main --> Input arguments != 2.") 
    
filename = sys.argv[1]
frame = cv2.imread(input_dir + filename)

blobs = generate_blobs(frame)
cc = CCL(blobs)
masks = generate_masks(cc)

#report_name = 
#report = None
#if not os.path.isfile("masks.rpt"):
#    report = open("masks.rpt", 'w')
#else
#    report = open("masks.rpt", 'a')
tokens = filename.split('.')
for m in range(0,len(masks)):
    output_filename = tokens[0] + "_m{}.".format(m) + tokens[1]
    output_filename = output_dir + output_filename

    cv2.imwrite(output_filename, masks[m])