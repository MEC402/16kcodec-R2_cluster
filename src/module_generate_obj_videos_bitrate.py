import os
from os import listdir
from os.path import isdir, join
import sys
import subprocess as sp
import pandas as pd
import re


bitrate_list = list(range(1000, 10000, 1000)) # Determines the bitrate for the video construction using FFMPEG

psnr_match_template = "speed="
size_match_template = "audio:0kB subtitle:0kB other streams"


if len(sys.argv) != 3:
    print(len(sys.argv))
    print("Usage: python module_generate_obj_videos_bitrate.py object_frames_path output_dir_path")
    raise Exception("GenerateObjVideosBitrate: main --> Input arguments != 3.") 



path = sys.argv[1]
output_dir = sys.argv[2]

directories = [f for f in listdir(path) if isdir(join(path, f))]

data_bitrate = pd.DataFrame(columns=['Id', 'bitrate_t', 'bitrate_r', 'Size', 'PSNR'])

for bitrate_t in bitrate_list:
    for d in directories:
        output = ' {}{}_{}.mp4'.format(output_dir, d, bitrate_t)
        cmd_options = "-i {}{}/%06d.png -r 30 -psnr -c:v mpeg4 -y ".format( path, d)
        current_opt = cmd_options + "-b:v " + str(bitrate_t)  + "k" +  output
        current_cmd = ['ffmpeg'] + current_opt.split(' ')
        result = sp.run(current_cmd, stderr=sp.PIPE)
        lines = result.stderr.splitlines()
        match = [s for s in lines if psnr_match_template in s.decode("utf-8")][-1]
        match = re.sub(' +', ' ', match.decode("utf-8"))
        match = re.sub('= +', '=', match).split(' ')
        psnr = match[6][2:]
        size = match[7][5:-2]
        bitrate_r = match[9][8:-7]
        data_bitrate = pd.concat( [ data_bitrate, pd.DataFrame([[int(d), float(bitrate_t), float(bitrate_r), float(size), float(psnr)]], columns=['Id', 'bitrate_t', 'bitrate_r', 'Size', 'PSNR']) ] )



data_bitrate.to_csv("{}/../quality_scores.csv".format(output_dir), sep=',', encoding='utf-8')   