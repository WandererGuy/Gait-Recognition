import os.path as osp
import time
import sys
from segment import *
import os 
import ast
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from fastapi import FastAPI, HTTPException, Form, Request
import uvicorn
import json 
import numpy as np
from utils.api_server import *
from external_api_server import pickle_path_seg
import configparser
config = configparser.ConfigParser()
current_script_directory = os.path.dirname(os.path.abspath(__file__))

config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
seg_port_num = config['DEFAULT']['seg_port_num'] 

pickle_path = os.path.join(current_script_directory,"pickle_variables")
pickle_path_seg = os.path.join(pickle_path, 'segment')

save_root = './demo/output/'
sil_save_path = save_root+'/GaitSilhouette/'


app = FastAPI()
def dict_keys2int(dict):
    # Access the 'gallery_track_result' dictionary
    # Convert all keys to integers
    dict = {int(k): v for k, v in dict.items()}
    return dict
    
@app.post("/segment-video") 
# have track result , have video
async def segment_video(request: Request):
    data = await request.json()
    video_path = data["video_path"]
    track_result_path = data["track_result_path"]
    with open(track_result_path, 'rb') as file:
        track_response_json = pickle.load(file)
        track_result = keys2int(track_response_json, 'track_result')
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
    silhouette = seg_modified(video_path, track_result, sil_save_path, save_video_name)
    segment_folder = sil_save_path + save_video_name
    sil_pickle_path = pickle_path_seg + save_video_name
    with open(sil_pickle_path, 'wb') as file:
        pickle.dump(silhouette, file)
    res = {"status": "success", "segment_folder": segment_folder, 'silhouette_pkl_path': sil_pickle_path}
    print ('Done Segment')
    return {'output': res}


@app.post("/extract-segment-folder") 
# already segment before , have segment folder
# or select out a segement sequence into a folder 
async def extract_segment_folder(request: Request):

    data = await request.json()
    segment_folder = data["segment_folder"]
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
    silhouette = getsil_modified(save_video_name, sil_save_path)
    segment_folder = sil_save_path + save_video_name
    with open(sil_pickle_path, 'wb') as file:
        pickle.dump(silhouette, file)

    sil_pickle_path = pickle_path_seg + save_video_name
    res = {"status": "success", "segment_folder": segment_folder, 'silhouette_pkl_path': sil_pickle_path}
    print ('Done Segment')
    return {'output': res}


@app.post("/segment-no-video") 
# dont have video
# only folder of cropped image of a single track target 
async def segment_no_video(request: Request):
    data = await request.json()
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
    tid = "001"
    folder_track_path = data["folder_track_path"] 
    sil_pickle_path = pickle_path_seg + save_video_name
    segment_folder = sil_save_path + save_video_name

    silhouette = seg_no_video(save_video_name, sil_save_path, tid, folder_track_path)
    with open(sil_pickle_path, 'wb') as file:
        pickle.dump(silhouette, file)
    res = {"status": "success","segment_folder": segment_folder, 'silhouette_pkl_path': sil_pickle_path}
    print ('Done Segment')
    return {'output': res}



def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_seg:app", host=host_ip, port=int(seg_port_num), reload=True)


if __name__ == "__main__":
    main()