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
from external_api_server import pickle_path

current_script_directory = os.path.dirname(os.path.abspath(__file__))

import configparser
config = configparser.ConfigParser()
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
seg_port_num = config['DEFAULT']['seg_port_num'] 


save_root = './demo/output/'
sil_save_path = save_root+'/GaitSilhouette/'


app = FastAPI()
def dict_keys2int(dict):
    # Access the 'gallery_track_result' dictionary
    

    # Convert all keys to integers
    dict = {int(k): v for k, v in dict.items()}

    return dict



class NumpyEncoder(json.JSONEncoder): # turn dict with np array to be jsonizable 
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
@app.post("/segment") 
# have track result , have video
async def segment(request: Request):

    data = await request.json()
    video_path = data["video_path"]
    track_result = data["track_result"]
    track_result = dict_keys2int(track_result)
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
    silhouette = seg_modified(video_path, track_result, sil_save_path, save_video_name)
    segment_folder = sil_save_path + save_video_name
    sil_pickle_path = pickle_path + save_video_name

    return_dict = {"segment_folder": segment_folder, 'silhouette_result':silhouette}
    pickle_response(response, seg_output_pickle)
    # res = json.dumps(return_dict, cls=NumpyEncoder)
    print ('Done Segment')
    return {'output': res}


@app.post("/extract-segment") 
# already segment before , have segment folder
# or select out a segement sequence into a folder 
async def extract_segment(request: Request):

    data = await request.json()
    track_result = data["track_result"]
    segment_folder = data["segment_folder"]
    track_result = dict_keys2int(track_result)
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
    silhouette = getsil_modified(save_video_name, sil_save_path)
    sil_pickle_path = pickle_path + save_video_name
    return_dict = {"segment_folder": segment_folder, 'silhouette_result':silhouette, "sil_pickle_path" : sil_pickle_path}
    res = json.dumps(return_dict, cls=NumpyEncoder)
    print ('Done Segment')
    return {'output': res}


@app.post("/segment-no-video") 
# dont have video
# only folder of cropped image of a single track target 
async def segment_no_video(request: Request):
    data = await request.json()
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
    tid = "001"
    folder_track_path = data["folder_track_path"] # path 
    sil_pickle_path = pickle_path + save_video_name
    segment_folder = sil_save_path + save_video_name

    silhouette = seg_no_video(save_video_name, sil_save_path, tid, folder_track_path)

    return_dict = {"segment_folder": segment_folder, 'silhouette_result':silhouette, "sil_pickle_path" : sil_pickle_path}

    res = json.dumps(return_dict, cls=NumpyEncoder)
    return {'output': res}



def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_seg:app", host=host_ip, port=int(seg_port_num), reload=True)


if __name__ == "__main__":
    main()