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

current_script_directory = os.path.dirname(os.path.abspath(__file__))

import configparser
config = configparser.ConfigParser()
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
rec_port_num = config['DEFAULT']['rec_port_num'] 




app = FastAPI()

save_root = './demo/output/'

import ast


def get_gait_feat(feat_dict:dict):
    all_embs = {}
    for key, value in feat_dict.items():
        path = os.path.join(gait_feat_folder,key,value,'undefined','undefined.pkl')
        embs = pickle.load(file = open(path, 'rb'))
        all_embs[f'{key}_{value}'] = embs
    return all_embs   

import torch
def computedistence(x, y):
    distance = torch.sqrt(torch.sum(torch.square(x - y)))
    return distance

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



gait_feat_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
result_distance_folder = gait_feat_folder + '/output/ResultDistance/'
gait_feat_folder = gait_feat_folder + '/output/GaitFeatures/'

@app.post("/compare-feats")
async def compare_feats(request: Request):
    '''
    with specific embs vs specific embs
    write distance into txt
    '''

    data = await request.json()
    gallery_feat_dict = data["gallery_feat_dict"]
    # {video_name:gait_id}
    probe1_feat_dict = data["probe1_feat_dict"]
    # {video_name:gait_id}
    gallery_feats = get_gait_feat(gallery_feat_dict)
    probe1_feats = get_gait_feat(probe1_feat_dict)
    with open (result_distance_folder + 'distance.txt', 'w') as file:
        for probe_key, probe_value in probe1_feats.items():
            for galler_key, gallery_value in gallery_feats.items():
                distance = computedistence(probe_value, gallery_value)
                file.write (f'{probe_key} vs {galler_key}: {distance}')
    
    
@app.post("/compare-multi-probe-video")
async def compare_multi_probe_video(request: Request):
    data = await request.json()
    video_save_folder = data["video_save_folder"] 
    # Get the value associated with the 'result' key

    list_probe_feat_path = data["list_probe_feat_path"]
    gallery_feat_path = data["gallery_feat_path"]
    list_distance_file_name = data["list_distance_file_name"]
    
    
    with open(gallery_feat_path, 'rb') as file:
        # Deserialize and retrieve the variable from the file
        gallery_feat = pickle.load(file)
    if 'video_save_folder' in gallery_feat:
        del gallery_feat['video_save_folder']
    
    for index, probe1_feat_path in enumerate(list_probe_feat_path):
    
            with open(probe1_feat_path, 'rb') as file:
                # Deserialize and retrieve the variable from the file
                probe1_feat = pickle.load(file)
            if 'video_save_folder' in probe1_feat:

                del probe1_feat['video_save_folder']
            gallery_probe1_result, all_compare = compare(probe1_feat, gallery_feat, mode = 'multi')
            # gallery_probe2_result = compare(probe2_feat, gallery_feat)
            # gallery_probe3_result = compare(probe3_feat, gallery_feat)
            # gallery_probe4_result = compare(probe4_feat, gallery_feat)

            write_distance_file = result_distance_folder + '/' + list_distance_file_name[index] + '.txt'
            with open(write_distance_file, 'w') as file:
                for key, value in all_compare.items():
                    file.write(key + ' : ' + str(value) + '\n')
                print ('result distance all videos written in ' + write_distance_file)


    return {'message': 'success'}





@app.post("/compare-feat-multi")
async def compare_feat_multi(request: Request):
    data = await request.json()
    video_save_folder = data["video_save_folder"] 
    # Get the value associated with the 'result' key

    probe1_feat_path = data["probe1_feat_path"]
    gallery_feat_path = data["gallery_feat_path"]
    distance_file_name = data["distance_file_name"]
    
    
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
    gallery_probe1_result, all_compare = compare(probe1_feat, gallery_feat, mode = 'multi')
    # gallery_probe2_result = compare(probe2_feat, gallery_feat)
    # gallery_probe3_result = compare(probe3_feat, gallery_feat)
    # gallery_probe4_result = compare(probe4_feat, gallery_feat)

    write_distance_file = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/ResultDistance'
    write_distance_file = write_distance_file + '/' + distance_file_name + '.txt'
    with open(write_distance_file, 'w') as file:
        for key, value in all_compare.items():
            file.write(key + ' : ' + str(value) + '\n')
    print ('result distance written in ' + write_distance_file)
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
    uvicorn.run("sample_rec:app", host=host_ip, port=int(rec_port_num), reload=True)

if __name__ == "__main__":
    main()