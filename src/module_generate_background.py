import cv2
import numpy as np
import pickle
from tracker import Tracker
from sklearn.cluster import DBSCAN
import video
import sys





    # If foreground (px, py) ==> True, otherwise False
def look_backward( px, py, f_curr):
      for f_it in range(f_curr, 0, -1):
            if f_it == 0: return False
            for o in tracker.getFrame(f_it).getObjects():
                  if o.is_pixel_in_object(px,py):
                        if not tracker.getFrame(f_it+1).is_object_in_frame(o):
                              return True
                        break
      return False

    # If foreground (px, py) ==> True, otherwise False
def look_forward(px, py, f_curr):
      max_frames = len(tracker.getFrames())
      for f_it in range(f_curr, max_frames):
            if f_it == max_frames: return False
            for o in tracker.getFrame(f_it).getObjects():
                  if o.is_pixel_in_object(px,py):
                        if not tracker.getFrame(f_it-1).is_object_in_frame(o):
                              return True
                        break
      return False
    


#%% MAIN METHOD

if len(sys.argv) != 6:
    print(len(sys.argv))
    print("Usage: python module_generate_background.py tracker_path src_dir_path output_dir_path tgt_width tgt_height")
    raise Exception("Generate background: main --> Input arguments != 6.") 
    
    
tracker_path = sys.argv[1]
src_dir = sys.argv[2]
output_dir = sys.argv[3]
tmp_dir = tracker_path[:-11] # remove the file from tracker_path to get the tmp dir

frame_width = int(sys.argv[4])
frame_heigth = int(sys.argv[5])

file = open(tracker_path, 'rb')
tracker = pickle.load(file)
file.close()

frame_count = len(tracker.getFrames())

#frame_foreground = [np.zeros((frame_heigth,frame_width), dtype=np.uint8) for _ in range(frame_count)] 
video_background = [np.zeros((frame_heigth,frame_width,3), dtype=np.uint8) for _ in range(frame_count)] 

for f in range(0,frame_count):
      #print(str(f) + " / " + str(frame_count))
      frame = cv2.imread("{}anim_{}_4k.png".format(src_dir, tracker.getFrame(f).getID()))
      for i in range(0, frame_heigth):
            for j in range(0, frame_width):
                  foreground = False
                  # Search for objects overlaping pixel i,j at frame f
                  for o in tracker.getFrame(f).getObjects():
                        if o.is_pixel_in_object(j,i):
                              foreground = True
                              break
                        
                        # Search for moving->stop objects
#                        if look_backward(i, j, f):
#                              foreground = True
##                        # Search for stopped->move objects 
##                        if look_forward(i, j, f):
##                              foreground = True
                  
                  if not foreground:
                        # assign the pixel as background
                        video_background[f][i,j] = frame[i,j] 




#%% PERFORM CLUSTERING FOR EACH PIXEL

video_background = np.array(video_background)
background = np.zeros((frame_heigth,frame_width,3), dtype=np.uint8)
pixel_data = [[video_background[:,i,j] for i in range(frame_heigth)] for j in range(frame_width)]

dbscan = DBSCAN(eps=10)
for i in range(0,frame_width):
      #print(i)
      for j in range(0,frame_heigth):
            dbscan.fit(pixel_data[i][j])
            labels = dbscan.labels_
            label_count = np.unique(labels, return_counts=True)
            max_label_idx = np.argmax(label_count[1])
            max_label = label_count[0][max_label_idx]
            pixel = []
            for x in range(len(pixel_data[i][j])):
                  if labels[x] == max_label:
                        pixel.append(pixel_data[i][j][x])
            background[j,i] = np.mean(np.array(pixel), axis=0)

#background = np.mean((np.array(frame_background).astype(np.float32)), axis=0)
cv2.imwrite("{}background.png".format(output_dir), background)

#%% SHOW BACKGROUND
#cv2.imshow("background", background)
#cv2.waitKey(0)
#cv2.destroyAllWindows()