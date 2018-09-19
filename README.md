# 16k codec in R2 cluster

This repository focuses on executing the 16k codec in the R2 cluster. I used _Snakemake_ to create multiple jobs that are launched in parallel. I will provide enough information about how to launch everthing but for deeper understanding go to the _Snakemake_ documentation: https://snakemake.readthedocs.io/en/stable/ .

## Requirements
This project uses some required libraries to work.:

* Python 3.5 (I installed from [Anaconda](https://www.anaconda.com/download/))
* OpenCV >3.3 (Using Python Pip and a [wheel](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv))
* [Snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html)

All of these requirements are already installed in R2. In the case we would like to change the cluster and use _Amazon Web Services_ (AWS), it is important to know that AWS supports _Snakemake_.

## Project structure (Important!)
_Snakemake_ makes use of two directories, an *output* directory and *temporal* directory for processing and a *source* directory to read the inputs. The *temporal* directory stores intermediate files required for the process and the *output* directory the reuslting files. The *source* directory must have all the frames in a lossless compressed format (.png). 

* The *temporal* directory has the following structure:
    * differences   --> stores contiguous frame differences
    * masks         --> stores generated object masks
    * object_frames --> stores cropped regions of the frame capturing each object


* While the *output* directory has the following one:
    * objects   --> stores tracked object videos 

## Running the project
To lauch the project using the following command inside the *src* directory to execute the _Snakemake_ jobs. Notice that it requires to pass some parameters.
```sh
$  RANGE=0,10 SRC_DIR=/scratch/ilopez/16k_video_source/ OUT_DIR=/scratch/ilopez/16k_output/ TMP_DIR=/scratch/ilopez/16k_tmp/ TGT_WIDTH=4096 TGT_HEIGHT=2018 snakemake
```
* RANGE: considering the uncompressed frames have unique ids, this parameter determines the starting frame and the ending frame to process. In this case, only 10 frames are going to be processed, from 0 to 10. (It only supports *anim_{id}_4k.png* like files)
* SRC_DIR: this variable is used to know the path to the source files in uncompressed format.
* OUT_DIR: this variable determines which is the directory in which the output files are going to be stored.
* TMP_DIR: this variable determines which is the directory in which the temporal files are going to be stored.
* TGT_WIDTH: the width of the video.
* TGT_HEIGHT: the height of the video.

I recommend to run this command from *home* directory and define the *source*, *output* and *temporal* directories in the */scratch/* drive. This ensures that the source code will not be removed from the file system while the output and temporal files may be deleted due to the R2 policies after a certain time.

## Future work
At this moment the project generates the compressed video in a single file. In the near future I will add the decoding part to the project.

In order to test the system with different bitrates, I will need to extend the project to compress individual object videos using *FFMPEG* library with different codecs and different bitrates. After that, I should be able to compute the *PSNR* score for the video and compare against the standard codecs using a *bitrate-PSNR* plot, where the *x* axis are the different bitrates and the *y* axis the quaility of the video.
