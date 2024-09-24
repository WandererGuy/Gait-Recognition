import os 
import os.path as osp
import sys
import cv2
from pathlib import Path
import shutil
# import torch
import math
import numpy as np
from tqdm import tqdm
import time 
import paddle 
# from tracking_utils.predictor import Predictor
# from yolox.utils import fuse_model, get_model_info
# from loguru import logger
# from tracker.byte_tracker import BYTETracker
# from tracking_utils.timer import Timer
# from tracking_utils.visualize import plot_tracking, plot_track
from pretreatment import pretreat, imgs2inputs
sys.path.append((os.path.dirname(os.path.abspath(__file__) )) + "/paddle/")
from seg_demo import seg_image_modified, seg_image
# from yolox.exp import get_exp
from parameters import config_gpu, seg_cfgs

from paddleseg.utils import get_sys_env, logger, get_image_list

def check_gpu_available():
    env_info = get_sys_env()
    print ('Paddle compiled with cuda:', env_info['Paddle compiled with cuda'] )
    print ('GPUs used:', env_info['GPUs used'])
    config_gpu = True if env_info['Paddle compiled with cuda'] \
        and env_info['GPUs used'] else False
    print ('config_gpu (use gpu) available:', config_gpu)


# def imageflow_single_frame(video_name, sil_save_path, tid, folder_track_path, frame_rate_segment):
#     # whole folder for 1 person , so 1 tid 
#     save_video_name = video_name
#     save_video_name = save_video_name.split(".")[0]
#     tidstr = "{:06d}".format(tid)
#     savesil_path = osp.join(sil_save_path, save_video_name, tidstr, "undefined")
    
#     # Read the image from a file
#     frame = cv2.imread(image)
#     tmp = frame
#     save_name = "{:06d}-{:06d}.png".format(tid, id)
#     # Get the dimensions of the image
#     # no need to extend crop like normal 
#     new_h, new_w, _ = tmp.shape
#     side = max(new_w,new_h)
#     tmp_new = [[[255,255,255]]*side]*side
#     tmp_new = np.array(tmp_new)
#     width = math.floor((side-new_w)/2)
#     height = math.floor((side-new_h)/2)
#     tmp_new[int(height):int(height+new_h),int(width):int(width+new_w),:] = tmp
#     tmp_new = tmp_new.astype(np.uint8)
#     tmp = cv2.resize(tmp_new,(192,192))
#     start = time.time()
#     seg_image(tmp, seg_cfgs["model"]["seg_model"], save_name, savesil_path, config_gpu)
#     # print ("seg_process_time 1 frame ", time.time() - start)
#     ch = cv2.waitKey(1)
#     if ch == 27 or ch == ord("q") or ch == ord("Q"):
#         break
#     return Path(sil_save_path, save_video_name)
def imageflow_demo_single_frame(image_path, save_image_path):
        frame = cv2.imread(image_path)
        tmp = frame
        # Get the dimensions of the image
        # no need to extend crop like normal 
        new_h, new_w, _ = tmp.shape
        side = max(new_w,new_h)
        tmp_new = [[[255,255,255]]*side]*side
        tmp_new = np.array(tmp_new)
        width = math.floor((side-new_w)/2)
        height = math.floor((side-new_h)/2)
        tmp_new[int(height):int(height+new_h),int(width):int(width+new_w),:] = tmp
        tmp_new = tmp_new.astype(np.uint8)
        tmp = cv2.resize(tmp_new,(192,192))
        start = time.time()
        seg_image_modified(tmp, seg_cfgs["model"]["seg_model"], save_image_path, config_gpu)
        # print ("seg_process_time 1 frame ", time.time() - start)
         


def imageflow_demo_no_video(video_name, sil_save_path, tid, folder_track_path, frame_rate_segment):
    # whole folder for 1 person , so 1 tid 
    save_video_name = video_name
    save_video_name = save_video_name.split(".")[0]
    tidstr = "{:06d}".format(tid)
    savesil_path = osp.join(sil_save_path, save_video_name, tidstr, "undefined")
    for id, filename in enumerate(tqdm(sorted(os.listdir(folder_track_path)))):
        if id % frame_rate_segment == 0:
            file_path = os.path.join(folder_track_path, filename)
            # Read the image from a file
            frame = cv2.imread(file_path)
            tmp = frame
            save_name = "{:06d}-{:06d}.png".format(tid, id)
            # Get the dimensions of the image
            # no need to extend crop like normal 
            new_h, new_w, _ = tmp.shape
            side = max(new_w,new_h)
            tmp_new = [[[255,255,255]]*side]*side
            tmp_new = np.array(tmp_new)
            width = math.floor((side-new_w)/2)
            height = math.floor((side-new_h)/2)
            tmp_new[int(height):int(height+new_h),int(width):int(width+new_w),:] = tmp
            tmp_new = tmp_new.astype(np.uint8)
            tmp = cv2.resize(tmp_new,(192,192))
            start = time.time()
            seg_image(tmp, seg_cfgs["model"]["seg_model"], save_name, savesil_path, config_gpu)
            # print ("seg_process_time 1 frame ", time.time() - start)
            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord("q") or ch == ord("Q"):
                break
    return Path(sil_save_path, save_video_name)

def imageflow_demo_modified(video_path, track_result, sil_save_path, save_video_name):
    """Cuts the video image according to the tracking result to obtain the silhouette

    Args:
        video_path (Path): Path of input video
        track_result (dict): Track information
        sil_save_path (Path): The root directory where the silhouette is stored
    Returns:
        Path: The directory of silhouette
    """
    
    
    cap = cv2.VideoCapture(video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_id = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    # save_video_name = video_path.split("/")[-1]

    # save_video_name = save_video_name.split(".")[0]
    results = []
    ids = list(track_result.keys()) # ids are frame id list 

    for i in tqdm(range(frame_count)):

        ret_val, frame = cap.read()
    
        if ret_val:
            if frame_id in ids and frame_id%4==0: # crop out of frame track target every 4 frames 

                for tidxywh in track_result[frame_id]:

                    '''
                    example 
                    [[2, 1574.658954852634, 229.29097154541995, 132.40578286636776, 318.3120958008027], 
                    [1, 636.3199330290356, 353.5785779473755, 408.22906522934807, 1056.940301610632], 
                    [3, 683.3798232245281, 881.7715030017587, 490.68301364590474, 687.7163959408705]]
                    '''

                    tid = tidxywh[0]
                    tidstr = "{:06d}".format(tid)
                    savesil_path = osp.join(sil_save_path, save_video_name, tidstr, "undefined")

                    x = tidxywh[1]
                    y = tidxywh[2]
                    width = tidxywh[3]
                    height = tidxywh[4]

                    x1, y1, x2, y2 = int(x), int(y), int(x + width), int(y + height)
                    w, h = x2 - x1, y2 - y1
                    
                    
                    # padding 10% to all sides (capture more around ROI)
                    x1_new = max(0, int(x1 - 0.1 * w))
                    x2_new = min(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(x2 + 0.1 * w))
                    y1_new = max(0, int(y1 - 0.1 * h))
                    y2_new = min(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(y2 + 0.1 * h))
                    
                    new_w = x2_new - x1_new
                    new_h = y2_new - y1_new
                    tmp = frame[y1_new: y2_new, x1_new: x2_new, :]

                    save_name = "{:06d}-{:06d}.png".format(tid, frame_id)
                    # place object in center of a square white image for padding 
                    # size sidexside to place cropped into later 
                    side = max(new_w,new_h)
                    tmp_new = [[[255,255,255]]*side]*side
                    tmp_new = np.array(tmp_new)
                    # calculate how much padding needed for each side left and right 
                    width = math.floor((side-new_w)/2) # floor is round up to int 
                    height = math.floor((side-new_h)/2)
                    tmp_new[int(height):int(height+new_h),int(width):int(width+new_w),:] = tmp
                    # so a white canvas with tmp in the center 
                    tmp_new = tmp_new.astype(np.uint8)
                    tmp = cv2.resize(tmp_new,(192,192))

                    start = time.time()
                    seg_image(tmp, seg_cfgs["model"]["seg_model"], save_name, savesil_path, config_gpu)
                    # print ("seg_process_time 1 frame ", time.time() - start)

            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord("q") or ch == ord("Q"):
                break
        else:
            break
        frame_id += 1
    return Path(sil_save_path, save_video_name)


def imageflow_demo(video_path, track_result, sil_save_path, save_video_name, frame_rate_segment):
    """Cuts the video image according to the tracking result to obtain the silhouette

    Args:
        video_path (Path): Path of input video
        track_result (dict): Track information
        sil_save_path (Path): The root directory where the silhouette is stored
    Returns:
        Path: The directory of silhouette
    """
    
    
    cap = cv2.VideoCapture(video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_id = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    # save_video_name = video_path.split("/")[-1]

    # save_video_name = save_video_name.split(".")[0]
    results = []
    ids = list(track_result.keys()) # ids are frame id list 

    for i in tqdm(range(frame_count)):

        ret_val, frame = cap.read()
    
        if ret_val:
            if frame_id in ids and frame_id%frame_rate_segment==0: # crop out of frame track target every 4 frames 
                for tidxywh in track_result[frame_id]:

                    '''
                    example 
                    [[2, 1574.658954852634, 229.29097154541995, 132.40578286636776, 318.3120958008027], 
                    [1, 636.3199330290356, 353.5785779473755, 408.22906522934807, 1056.940301610632], 
                    [3, 683.3798232245281, 881.7715030017587, 490.68301364590474, 687.7163959408705]]
                    '''

                    tid = tidxywh[0]
                    tidstr = "{:06d}".format(tid)
                    savesil_path = osp.join(sil_save_path, save_video_name, tidstr, "undefined")

                    x = tidxywh[1]
                    y = tidxywh[2]
                    width = tidxywh[3]
                    height = tidxywh[4]

                    x1, y1, x2, y2 = int(x), int(y), int(x + width), int(y + height)
                    w, h = x2 - x1, y2 - y1
                    
                    
                    # padding 10% to all sides (capture more around ROI)
                    x1_new = max(0, int(x1 - 0.1 * w))
                    x2_new = min(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(x2 + 0.1 * w))
                    y1_new = max(0, int(y1 - 0.1 * h))
                    y2_new = min(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(y2 + 0.1 * h))
                    
                    new_w = x2_new - x1_new
                    new_h = y2_new - y1_new
                    tmp = frame[y1_new: y2_new, x1_new: x2_new, :]

                    save_name = "{:06d}-{:06d}.png".format(tid, frame_id)
                    # place object in center of a square white image for padding 
                    # size sidexside to place cropped into later 
                    side = max(new_w,new_h)
                    tmp_new = [[[255,255,255]]*side]*side
                    tmp_new = np.array(tmp_new)
                    # calculate how much padding needed for each side left and right 
                    width = math.floor((side-new_w)/2) # floor is round up to int 
                    height = math.floor((side-new_h)/2)
                    tmp_new[int(height):int(height+new_h),int(width):int(width+new_w),:] = tmp
                    # so a white canvas with tmp in the center 
                    tmp_new = tmp_new.astype(np.uint8)
                    tmp = cv2.resize(tmp_new,(192,192))

                    start = time.time()
                    seg_image(tmp, seg_cfgs["model"]["seg_model"], save_name, savesil_path, config_gpu)
                    # print ("seg_process_time 1 frame ", time.time() - start)

            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord("q") or ch == ord("Q"):
                break
        else:
            break
        frame_id += 1
    return Path(sil_save_path, save_video_name)



def seg(video_path, track_result, sil_save_path):
    """Cuts the video image according to the tracking result to obtain the silhouette

    Args:
        video_path (Path): Path of input video
        track_result (Path): Track information
        sil_save_path (Path): The root directory where the silhouette is stored
    Returns:
        inputs (list): List of Tuple (seqs, labs, typs, vies, seqL) 
    """
    
    sil_save_path = imageflow_demo(video_path, track_result, sil_save_path)

    inputs = imgs2inputs(Path(sil_save_path), 64, False, seg_cfgs["gait"]["dataset"])
    return inputs

def seg_single_frame(image_path, save_image_path):
    imageflow_demo_single_frame(image_path,
                                save_image_path
                                )
    # inputs = imgs2inputs(Path(sil_save_path), 64, False, seg_cfgs["gait"]["dataset"])
     

def seg_no_video(video_name, sil_save_path, folder_track_path, frame_rate_segment):
    tid = 1

    sil_save_path = imageflow_demo_no_video(video_name, 
                                            sil_save_path, 
                                            tid, 
                                            folder_track_path, 
                                            frame_rate_segment) 


    inputs = imgs2inputs(Path(sil_save_path), 64, False, seg_cfgs["gait"]["dataset"])
    return inputs
def getsil(video_path, sil_save_path):
    sil_save_name = Path(video_path).name
    inputs = imgs2inputs(Path(sil_save_path, sil_save_name.split(".")[0]), 
                64, False, seg_cfgs["gait"]["dataset"])
    return inputs

def getsil_no_video(sil_save_path):
    inputs = imgs2inputs(Path(sil_save_path), 
                64, False, seg_cfgs["gait"]["dataset"])
    return inputs

def getsil_modified(sil_save_path):
    inputs = imgs2inputs(Path(sil_save_path), 
                64, False, seg_cfgs["gait"]["dataset"])
    return inputs


def seg_modified(video_path, track_result, sil_save_path, save_video_name, frame_rate_segment):
    """Cuts the video image according to the tracking result to obtain the silhouette

    Args:
        video_path (Path): Path of input video
        track_result (Path): Track information
        sil_save_path (Path): The root directory where the silhouette is stored
    Returns:
        inputs (list): List of Tuple (seqs, labs, typs, vies, seqL) 
    """
    
    sil_save_path = imageflow_demo(video_path, track_result, sil_save_path, save_video_name, frame_rate_segment)
    inputs = imgs2inputs(Path(sil_save_path), 64, False, seg_cfgs["gait"]["dataset"])
    return inputs
