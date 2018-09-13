# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:11:49 2018

@author: IkerVazquezlopez
"""

import sys
import pickle
import cv2
import numpy as np




#%% MAIN METHOD


if len(sys.argv) != 2:
    print(len(sys.argv))
    print("Usage: python module_decode_streams.py file_stream")
    raise Exception("Stream decoder: main --> Input arguments != 2.") 
    
    
binary = open(sys.argv[1], 'rb')

target_w = int.from_bytes(binary.read(2), byteorder='big')
target_h = int.from_bytes(binary.read(2), byteorder='big')
target_size = size = int.from_bytes(binary.read(4), byteorder='big')
data = int.from_bytes(binary.read(target_size), byteorder='big')
target_back = np.frombuffer(data, dtype=np.uint8)
target_back = cv2.decode(target_back)
target_back = target_back.reshape((target_h, target_w,3))

n_frames = int.from_bytes(binary.read(8), byteorder='big')

for _ in range(0, n_frames):
    n_objects = int.from_bytes(binary.read(2), byteorder='big')
    for _ in range(0, n_objects):
        obj_id = int.from_bytes(binary.read(2), byteorder='big')
        x = int.from_bytes(binary.read(2), byteorder='big')
        y = int.from_bytes(binary.read(2), byteorder='big')
        w = int.from_bytes(binary.read(2), byteorder='big')
        h = int.from_bytes(binary.read(2), byteorder='big')
        size = int.from_bytes(binary.read(4), byteorder='big')
        data = int.from_bytes(binary.read(size), byteorder='big')
        img = np.frombuffer(data, dtype=np.uint8)
        img = cv2.decode(img)
        img = img.reshape((h,w,3))
    
    
binary.close()
    


        