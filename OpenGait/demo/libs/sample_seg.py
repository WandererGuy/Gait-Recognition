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

host_ip = '10.0.68.103'
port_num = 8502



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
    save_root = './demo/output/'
    gallery_video_path = data["gallery_video_path"]

    # gallery_video_path = "./demo/output/InputVideos/gallery.mp4"
    # probe1_video_path  = "./demo/output/InputVideos/probe1.mp4"
    # probe2_video_path  = "./demo/output/InputVideos/probe2.mp4"
    # probe3_video_path  = "./demo/output/InputVideos/probe3.mp4"
    # probe4_video_path  = "./demo/output/InputVideos/probe4.mp4"

    # # Get the value associated with the 'result' key

    gallery_track_result = data["gallery_track_result"]
    # probe1_track_result = data["probe1_track_result"]
    # probe2_track_result = data["probe2_track_result"]
    # probe3_track_result = data["probe3_track_result"]
    # probe4_track_result = data["probe4_track_result"]
    video_save_folder = data["video_save_folder"]

    gallery_track_result = dict_keys2int(gallery_track_result)
    # probe1_track_result = dict_keys2int(probe1_track_result)


    gallery_video_name = gallery_video_path.split("/")[-1]
    gallery_video_name = save_root+'/GaitSilhouette/'+gallery_video_name.split(".")[0]
    # probe1_video_name  = probe1_video_path.split("/")[-1]
    # probe1_video_name  = save_root+'/GaitSilhouette/'+probe1_video_name.split(".")[0]
    # probe2_video_name  = probe2_video_path.split("/")[-1]
    # probe2_video_name  = save_root+'/GaitSilhouette/'+probe2_video_name.split(".")[0]
    # probe3_video_name  = probe3_video_path.split("/")[-1]
    # probe3_video_name  = save_root+'/GaitSilhouette/'+probe3_video_name.split(".")[0]
    # probe4_video_name  = probe4_video_path.split("/")[-1]
    # probe4_video_name  = save_root+'/GaitSilhouette/'+probe4_video_name.split(".")[0]
    # exist = os.path.exists(gallery_video_name) and os.path.exists(probe1_video_name) \
    #         and os.path.exists(probe2_video_name) and os.path.exists(probe3_video_name) \
    #         and os.path.exists(probe4_video_name)
    # exist = os.path.exists(gallery_video_name) and os.path.exists(probe1_video_name)
    exist = os.path.exists(gallery_video_name) 

    print(exist)
    if exist:
        gallery_silhouette = getsil(gallery_video_path, save_root+'/GaitSilhouette/')
        # probe1_silhouette  = getsil(probe1_video_path , save_root+'/GaitSilhouette/')
        # probe2_silhouette  = getsil(probe2_video_path , save_root+'/GaitSilhouette/')
        # probe3_silhouette  = getsil(probe3_video_path , save_root+'/GaitSilhouette/')
        # probe4_silhouette  = getsil(probe4_video_path , save_root+'/GaitSilhouette/')
    else:
        gallery_silhouette = seg(gallery_video_path, gallery_track_result, save_root+'/GaitSilhouette/')
        # probe1_silhouette  = seg(probe1_video_path , probe1_track_result , save_root+'/GaitSilhouette/')
        # probe2_silhouette  = seg(probe2_video_path , probe2_track_result , save_root+'/GaitSilhouette/')
        # probe3_silhouette  = seg(probe3_video_path , probe3_track_result , save_root+'/GaitSilhouette/')
        # probe4_silhouette  = seg(probe4_video_path , probe4_track_result , save_root+'/GaitSilhouette/')

    return_dict = {
                    'gallery_silhouette':gallery_silhouette, 
                #    'probe1_silhouette': probe1_silhouette,
                #    'probe2_silhouette': probe2_silhouette,
                #    'probe3_silhouette': probe3_silhouette,
                #    'probe4_silhouette': probe4_silhouette, 
                   'video_save_folder': video_save_folder}
    
    dump = json.dumps(return_dict, cls=NumpyEncoder)


    print ('Done Segment')
    return {'output': dump}

def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_seg:app", host=host_ip, port=int(port_num), reload=True)


if __name__ == "__main__":
    main()