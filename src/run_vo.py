import os
import sys
import cv2
import math
import numpy as np
import argparse

sys.path.append('../pyslam/')
from config import Config
from visual_odometry import VisualOdometry
from camera  import PinholeCamera
from ground_truth import groundtruth_factory
from dataset import dataset_factory
import matplotlib.pyplot as plt
from glob import glob

from feature_tracker import feature_tracker_factory, FeatureTrackerTypes 
from feature_manager import feature_manager_factory
from feature_types import FeatureDetectorTypes, FeatureDescriptorTypes, FeatureInfo
from feature_matcher import feature_matcher_factory, FeatureMatcherTypes
from tqdm import tqdm
from feature_tracker_configs import FeatureTrackerConfigs

parser = argparse.ArgumentParser(description='Run VO')
parser.add_argument('--n', type=str, default='default', help='experimet name')

args = parser.parse_args()
exp_name = args.n

model_config = {
    'LK_FAST': FeatureTrackerConfigs.LK_FAST,
    'LK_SHI_TOMASI': FeatureTrackerConfigs.LK_SHI_TOMASI,
}

folders = os.listdir('../data/dataset/sequences/')
folders.sort()

for f in folders:
    print('Folder: ',f)
    config = Config(f)

    dataset = dataset_factory(config.dataset_settings)
    groundtruth = groundtruth_factory(config.dataset_settings)

    cam = PinholeCamera(config.cam_settings['Camera.width'], config.cam_settings['Camera.height'],
                        config.cam_settings['Camera.fx'], config.cam_settings['Camera.fy'],
                        config.cam_settings['Camera.cx'], config.cam_settings['Camera.cy'],
                        config.DistCoef, config.cam_settings['Camera.fps'])

    num_features=2000  # how many features do you want to detect and track?

    # select your tracker configuration (see the file feature_tracker_configs.py) 
    # LK_SHI_TOMASI, LK_FAST
    # SHI_TOMASI_ORB, FAST_ORB, ORB, BRISK, AKAZE, FAST_FREAK, SIFT, ROOT_SIFT, SURF, SUPERPOINT, FAST_TFEAT
    tracker_config = model_config[exp_name]
    tracker_config['num_features'] = num_features

    feature_tracker = feature_tracker_factory(**tracker_config)
    # create visual odometry object 
    vo = VisualOdometry(cam, groundtruth, feature_tracker)

    # todo: add the trajectory visualization
    traj_img_size = 800
    traj_img = np.zeros((traj_img_size, traj_img_size, 3), dtype=np.uint8)
    half_traj_img_size = int(0.5*traj_img_size)
    draw_scale = 1

    # second loop for iterating over all the frame
    result = []  
    for img_id in tqdm(range(dataset.max_frame_id)):
        img = dataset.getImage(img_id)
        if img is not None:
            vo.track(img, img_id)
            tmp = np.reshape(np.hstack((vo.cur_R, vo.cur_t)), 12)
            result.append(' '.join([str(i) for i in tmp]))

    # Save the results in the text files
    res_base_path = os.path.join('../data/results/', exp_name)
    res_folder_path = os.path.join(res_base_path, f+'.txt')
    os.makedirs(res_base_path, exist_ok=True)

    txt_file=open(res_folder_path, 'a') 
    txt_file.writelines("%s\n" % i for i in result) 
    txt_file.close() 