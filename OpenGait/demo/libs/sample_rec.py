import os
import os.path as osp
import time
import sys
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from recognise import *
import requests
import json 
from fastapi import FastAPI, HTTPException, Form, Request
import uvicorn


host_ip = '10.0.68.103'
port_num = 8503

app = FastAPI()

save_root = './demo/output/'

import ast
def str2dict(string_dict):
    # actual_dict = ast.literal_eval(string_dict)
    actual_dict = json.loads(string_dict)
    return actual_dict
@app.post("/extract-sil-function")
async def extract_sil_function(request: Request):
    data = await request.json()

    # Get the value associated with the 'result' key
    rec_output_pickle = data["rec_output_pickle"]

    data = data["output"]
    # Convert JSON string to dictionary

    data = json.loads(data)
    gallery_silhouette = data["gallery_silhouette"]
    # probe1_silhouette  = data["probe1_silhouette"]
    # probe2_silhouette  = data["probe2_silhouette"]
    # probe3_silhouette  = data["probe3_silhouette"]
    # probe4_silhouette  = data["probe4_silhouette"]
    video_save_folder = data["video_save_folder"]

    # recognise
    video_feat = extract_sil(gallery_silhouette, save_root+'/GaitFeatures/')
    # probe1_feat  = extract_sil(probe1_silhouette , save_root+'/GaitFeatures/')
    # probe2_feat  = extract_sil(probe2_silhouette , save_root+'/GaitFeatures/')
    # probe3_feat  = extract_sil(probe3_silhouette , save_root+'/GaitFeatures/')
    # probe4_feat  = extract_sil(probe4_silhouette , save_root+'/GaitFeatures/')
    video_feat["video_save_folder"] = video_save_folder
    print ('done recognise')
    with open(rec_output_pickle, 'wb') as file:
    # Serialize and write the variable to the file
        pickle.dump(video_feat, file)

    return {"message": "success"}

@app.post("/compare-feat-multi")
async def compare_feat_multi(request: Request):
    data = await request.json()
    video_save_folder = data["video_save_folder"] 
    # Get the value associated with the 'result' key

    probe1_feat_path = data["probe1_feat_path"]
    gallery_feat_path = data["gallery_feat_path"]
    
    
    
    with open(gallery_feat_path, 'rb') as file:
        # Deserialize and retrieve the variable from the file
        gallery_feat = pickle.load(file)
    if 'video_save_folder' in gallery_feat:
        del gallery_feat['video_save_folder']

    with open(probe1_feat_path, 'rb') as file:
        # Deserialize and retrieve the variable from the file
        probe1_feat = pickle.load(file)
    if 'video_save_folder' in probe1_feat:

        del probe1_feat['video_save_folder']
    gallery_probe1_result = compare(probe1_feat, gallery_feat, mode = 'multi')
    # gallery_probe2_result = compare(probe2_feat, gallery_feat)
    # gallery_probe3_result = compare(probe3_feat, gallery_feat)
    # gallery_probe4_result = compare(probe4_feat, gallery_feat)



    output = {
        "gallery_probe1_result": gallery_probe1_result,
        # "gallery_probe2_result": gallery_probe2_result,
        # "gallery_probe3_result": gallery_probe3_result,
        # "gallery_probe4_result": gallery_probe4_result,
        "video_save_folder": video_save_folder
    }


    return {"output": output}

@app.post("/compare-feat-single")
async def compare_feat_single(request: Request):
    data = await request.json()
    id = data["id"]
    video_save_folder = data["video_save_folder"] 
    # Get the value associated with the 'result' key
    mode = data["mode"]
    probe1_feat_path = data["probe1_feat_path"]
    gallery_feat_path = data["gallery_feat_path"]

    with open(probe1_feat_path, 'rb') as file:
        # Deserialize and retrieve the variable from the file
        probe1_feat = pickle.load(file)
    with open(gallery_feat_path, 'rb') as file:
        # Deserialize and retrieve the variable from the file
        gallery_feat = pickle.load(file)

        target_feat = {'gallery':[{id: {'undefined': gallery_feat }}]}  

    if 'video_save_folder' in probe1_feat:
        del probe1_feat['video_save_folder']
        
    gallery_probe1_result = compare(probe1_feat, target_feat, mode = mode)
    # gallery_probe2_result = compare(probe2_feat, gallery_feat)
    # gallery_probe3_result = compare(probe3_feat, gallery_feat)
    # gallery_probe4_result = compare(probe4_feat, gallery_feat)

    output = {
        "gallery_probe1_result": gallery_probe1_result,
        # "gallery_probe2_result": gallery_probe2_result,
        # "gallery_probe3_result": gallery_probe3_result,
        # "gallery_probe4_result": gallery_probe4_result,
        "video_save_folder": video_save_folder
    }


    return {"output": output}        

def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_rec:app", host=host_ip, port=int(port_num), reload=True)

if __name__ == "__main__":
    main()