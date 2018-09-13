


import cv2
import numpy as np
import sys
import os
from os import listdir
from os.path import isfile, join


def get_int(name):
      i = name.split('_')[1]
      return(int(i))

def PSNR(input_signal, noisy_signal):
      max_in_signal = np.max(input_signal)**2
      mse = np.mean(((input_signal - noisy_signal) * (input_signal - noisy_signal)))
      return 10* np.log(max_in_signal / mse)








if len(sys.argv) != 3:
    print(len(sys.argv))
    print("Usage: python test_quality.py original_dir comparison_dir")
    raise Exception("Test Quality: main --> Input arguments != 3.") 
    
original_dir = sys.argv[1]
comparison_dir = sys.argv[2]

filenames = [f for f in listdir(original_dir) if isfile(join(original_dir, f))]
filenames.sort(key=get_int)
    
frame_psnr = []
for frame_name in filenames:
    id = get_int(frame_name)
    print(id)
    orig_frame = cv2.imread(original_dir + frame_name)
    if not os.path.exists(comparison_dir + str(id) + ".png"):
        continue
    comp_frame = cv2.imread(comparison_dir + str(id) + ".png")
    frame_psnr.append( PSNR(orig_frame, comp_frame) )
    
    
print( np.mean(frame_psnr) )
    
    
