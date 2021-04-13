# VO_benchmark
This repository holds all the code for our [EECS 568: Mobile Robotics]() final project

[**VO_benchmark: Impact of Image Feature Detector and Descriptor Choice on Visual Odometry**]()   
Chunkai Yao, [Danish Syed](https://dysdsyd.github.io), Joseph Kim, Peerayos Pongsachai, Teerachart Soratana

## Installation
Please follow the instructions from [pySLAM v2](https://github.com/luigifreda/pyslam/blob/master/CONDA.md) repository. Our implementation uses the [conda environment installation](https://github.com/luigifreda/pyslam/blob/master/CONDA.md).


## Datasets
We used the first 10 (00-10) trajectory sequences from KITTI dataset for evlaution. Download the [KITTI odometry data set (grayscale, 22 GB)](http://www.cvlibs.net/datasets/kitti/eval_odometry.php) and store it in the `data/dataset` folder with the following directory structure.
```
├── data/dataset
    ├── sequences
        ├── 00
        ...
        ├── 21
    ├── poses
        ├── 00.txt
            ...
        ├── 10.txt

```

## Usage Instructions
Once installed, there are two steps to generate the Visual Odometry (VO) results on the KITTI dataset. 

#### (1) Running the VO for multiple Detector and Descriptor Combinations
1. Create the descriptor and detector configurations in the `test_configs` dictionary present in `pyslam/feature_tracker_configs.py` 
2. Run VO experiment over all the trajectory sequences by:
```
$ cd src
$ python run_vo.py
```
The ouput will be dumped into the `data/dataset/results` folder.

#### (2) Evaluating the VO for multiple Detector and Descriptor Combinations
[WIP]


## Acknowledgements
The autors would like to thank the [luigifreda/pyslam](https://github.com/luigifreda/pyslam) repository for collating multiple Visual Odometry feature detectors and descriptors.
