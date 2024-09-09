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


current_script_directory = os.path.dirname(os.path.abspath(__file__))

import configparser
config = configparser.ConfigParser()
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
seg_port_num = config['DEFAULT']['seg_port_num'] 


save_root = './demo/output/'


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
async def segment(request: Request):

    data = await request.json()
    video_path = data["video_path"]
    # # Get the value associated with the 'result' key
    track_result = data["track_result"]
    track_result = dict_keys2int(track_result)
    video_name = video_path.split("/")[-1]
    video_new_path = save_root+'/GaitSilhouette/' + video_name.split(".")[0]
    exist = os.path.exists(video_new_path) 

    print("segment folder exists: " ,exist)
    if exist:
        silhouette = getsil(video_path, save_root+'/GaitSilhouette/')
    else:
        silhouette = seg(video_path, track_result, save_root+'/GaitSilhouette/')

    return_dict = {'silhouette':silhouette}
    dump = json.dumps(return_dict, cls=NumpyEncoder)
    print ('Done Segment')
    return {'output': dump}


@app.post("/segment-no-video")
async def segment_no_video(request: Request):
    try:
        data = await request.json()
        video_name = data["choose_video_name"]
        tid = data["tid"]
        folder_track_path = data["folder_track_path"] # path 
        sil_images_folder = save_root+'/GaitSilhouette/'+ video_name
        exist = os.path.exists(sil_images_folder) 

        print("segment folder exists: " ,exist)
        if exist:
            silhouette = getsil_no_video(video_name, save_root+'/GaitSilhouette/')
        else:
            silhouette = seg_no_video(video_name, save_root+'/GaitSilhouette/', tid, folder_track_path)

        return_dict = {
                        'silhouette':silhouette, 
                        }    
        dump = json.dumps(return_dict, cls=NumpyEncoder)
        return {'output': dump}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_seg:app", host=host_ip, port=int(seg_port_num), reload=True)


if __name__ == "__main__":
    main()