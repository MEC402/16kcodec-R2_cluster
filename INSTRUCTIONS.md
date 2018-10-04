# INSTRUCTIONS (step by step)

## Requirements
This project uses some required libraries to work.:

* Python 3.5 (I installed from [Anaconda](https://www.anaconda.com/download/))
* OpenCV >3.3 (Using Python Pip and a [wheel](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv))
* [Snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html)
* [FFMPEG](https://www.ffmpeg.org/)

All of these requirements are already installed in the R2 cluster. 
In the case we would like to change the cluster and use _Amazon Web Services_ (AWS) we should install all of the libraries, it is important to note that AWS supports _Snakemake_.



## Create the directory structure for temporal and output files
This project requires an specific directory structure to store partial and final results. 

1. Assuming that the user has access to the _/scratch/_ direcotry in R2, create a folder to store all the results named **16k_results**.
2. Inside **16k_results** create three new directories named **video\_source**, **tmp** and **out**.
3. Let's focus on the **tmp** directory and inside it create three folders named: **differences**, **masks** and **object_frames**.
	- **differences** stores frame differences respect to the previous frame.
	- **masks** stores detected object binary masks.
	- **object\_frames** stores cropped frames of detected objects in the video.
4. Now in **out** directory create a folder named **objects** which is used to store each object's video.
5. Finally, in the **video\_source** directory, add all the video frames in *.png* format with no compression and name them as *anim_{f}_{r}k.png*, where *f* is the frame number and *r* the resolution (e.g. 2k, 4k, 8k, 16k). **At this moment *r* = 4!!**
	- The six digit number have to match with the frame number in the video. If that is not the case, FFMPEG will raise an error.
}

After following these instructions, the final structure should be as the following one:
```
/scratch/{user}/16k_results 
│
└─── tmp
│   │   differences
│   │   masks
│   │	object_frames
│   
└─── out
│   │   objects
│
└─── video_source
    │   anim_0_4k.png
	│   anim_1_4k.png
    │	...
```


## Running the program
To launch the program and execute the _Snakemake_ jobs use the following command inside the **src** directory. Notice that it requires to pass some parameters.
```sh
$  RANGE=0,10 SRC_DIR=/scratch/{user}/16k_results/video_source/ OUT_DIR=/scratch/{user}/16k_results/out/ TMP_DIR=/scratch/{user}/16k_results/tmp TGT_WIDTH=4096 TGT_HEIGHT=2018 snakemake
```
* **RANGE**: considering the uncompressed frames have unique ids, this parameter determines the starting frame and the ending frame to process. In this case, only 10 frames are going to be processed, from 0 to 10. (It only supports *anim_{id}_4k.png* like files)
* **SRC_DIR**: this variable is used to know the path to the source files in uncompressed format.
* **OUT_DIR**: this variable determines which is the directory in which the output files are going to be stored.
* **TMP_DIR**: this variable determines which is the directory in which the temporal files are going to be stored.
* **TGT_WIDTH**: the width of the video.
* **TGT_HEIGHT**: the height of the video.


## Collecting the results
Once the program has finished, inside **/scratch/{user}/16k\_results/out/objects/** are stored each video object compressed with different bitrates. The naming of those videos is as follows: *{id}_{bitrate}.mp4*, where *id* is the object id and *bitrate* the target bitrate used for compressing using FFMEG.

Finally, in **/scratch/{user}/16k\_results/out/** two files were created: *background.png* which is an image of the video background, and *quality_scores.csv* which collects the target bitrate, real bitrate, size and PSNR (quality) score of each object video.

If the user wants to keep those results, I will encourage to copy them to another file system because in **/scratch/** can be removed.

