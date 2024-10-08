print("............. Initialization .............")
from fastapi import FastAPI, HTTPException, Form, Request
app = FastAPI()

import os
import sys
from utils_server.api_server import *
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from recognise import extract_sil_modified, compare
import uvicorn
import configparser
import logging 
from tqdm import tqdm
from pathlib import Path
from typing import List


current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_folder = os.path.dirname(current_script_directory)

config = configparser.ConfigParser()
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
rec_port_num = config['DEFAULT']['rec_port_num'] 

save_root = './demo/output/'
gait_feat_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pickle_path = os.path.join(current_script_directory,"pickle_variables")
compare_session_folder = os.path.join(pickle_path, 'CompareSession/')
pickle_path_rec = os.path.join(pickle_path, "embeddings_db")
os.makedirs(save_root, exist_ok=True)
os.makedirs(pickle_path, exist_ok=True)
os.makedirs(pickle_path_rec, exist_ok=True)
os.makedirs(compare_session_folder, exist_ok=True)
print(".............Initialization complete.............")


@app.post("/extract-sil-function-v0")
async def extract_sil_function_v0(sil_pickle_path: str = Form(...)):
    sil_pickle_path = Path(sil_pickle_path)
    tmp = sil_pickle_path.name.split(".")[0]
    rec_output_pickle = os.path.join(pickle_path_rec, tmp + ".pkl")
    with open (sil_pickle_path, 'rb') as file:
        silhouette = pickle.load(file)
    if silhouette != []:
        # recognise
        # if not os.path.exists(rec_output_pickle):
        video_feat = extract_sil_modified(silhouette)
        with open(rec_output_pickle, 'wb') as file:
            pickle.dump(video_feat, file)
        print ('done recognise')

        res = {
                "status": 1,
                "error_code": None,
                "error_message": None,
                "result":
                    {
                        "embedding_path": fix_path(rec_output_pickle)
                    }
                }
    else: 
        res = {
                "status": 0,
                "error_code": 400,
                "error_message": "Sil result is empty already, check segment phase again",
                "result": None
                } 
    return res

@app.post("/extract-sil-function")
async def extract_sil_function(sil_pickle_path: str = Form(...)):
    sil_pickle_path = Path(sil_pickle_path)
    tmp = sil_pickle_path.name.split(".")[0]
    rec_output_pickle = os.path.join(pickle_path_rec, tmp + ".pkl")
    with open (sil_pickle_path, 'rb') as file:
        silhouette = pickle.load(file)
    if silhouette != []:
        # recognise
        # if not os.path.exists(rec_output_pickle):
        video_feat = extract_sil_modified(silhouette)
        with open(rec_output_pickle, 'wb') as file:
            pickle.dump(video_feat, file)
        
        value1=video_feat[list(video_feat.keys())[0]][0][list(video_feat[list(video_feat.keys())[0]][0].keys())[0]][list(video_feat[list(video_feat.keys())[0]][0][list(video_feat[list(video_feat.keys())[0]][0].keys())[0]].keys())[0]].cpu()

        flattened_array = value1.numpy().flatten()
        string_emb=str(flattened_array[0])
        for i in range(1,len(flattened_array),1):
            string_emb=string_emb+","+str(flattened_array[i])
        print ('done recognise')

        res = {
                "status": 1,
                "error_code": None,
                "error_message": None,
                "result":
                    {
                        "embedding_path": string_emb
                    }
                }
    else: 
        res = {
                "status": 0,
                "error_code": 400,
                "error_message": "Sil result is empty already, check segment phase again",
                "result": None
                } 
    return res

@app.post("/compare-embeddings")
async def compare_embeddings(
                            probe_feat_path: str = Form(...), 
                            list_gallery_feat_path: List[str]  = Form(...)
                            ):
    compare_session = generate_unique_filename(UPLOAD_FOLDER = compare_session_folder, extension=None)
    probe_feat_path = Path(probe_feat_path)
    compare_session_save_path, ranking_ls = compare_multi_gallery_modified(
                         compare_session = compare_session,
                         probe_feat_path = probe_feat_path, 
                         list_gallery_feat_path = list_gallery_feat_path, 
                         )
    print ('done compare')
            
    res = {
            "status": 1,
            "error_code": None,
            "error_message": None,
            "result": 
                {
                "ranking_ls": ranking_ls,
                "compare_session_save_path": fix_path(compare_session_save_path)
                }
            }

    return res

@app.post("/compare-embeddings-short")
async def compare_embeddings(
                            probe_feat_path: str = Form(...), 
                            list_gallery_feat_path: str  = Form(...)
                            ):
    compare_session = generate_unique_filename(UPLOAD_FOLDER = compare_session_folder, extension=None)
    probe_feat_path = Path(probe_feat_path)
    compare_session_save_path, ranking_ls = compare_multi_gallery_modified(
                         compare_session = compare_session,
                         probe_feat_path = probe_feat_path, 
                         list_gallery_feat_path = [list_gallery_feat_path], 
                         )
    print ('done compare')
            
    res = {
            "status": 1,
            "error_code": None,
            "error_message": None,
            "result": 
                {
                "distance": ranking_ls[0]["distance"],
                }
            }

    return res


def compare_multi_gallery_modified(compare_session, probe_feat_path, list_gallery_feat_path):
    input_compare_json = {"probe_feat_path": probe_feat_path,
                          "list_gallery_feat_path": list_gallery_feat_path, 
                          "session": compare_session}
    compare_session_save_path = compare_multi_gallery_video(input_compare_json)
    return compare_session_save_path


def compare_multi_gallery_video(data: dict):
    session = data["session"]
    list_gallery_feat_path = data["list_gallery_feat_path"]
    probe_feat_path = data["probe_feat_path"]
    with open(probe_feat_path, 'rb') as file:
        probe_feat = pickle.load(file)
    item_ls = []
    for index, gallery_feat_path in enumerate(tqdm(list_gallery_feat_path)):
            gallery_feat_path = Path(gallery_feat_path)
            if os.path.exists(gallery_feat_path):  
                with open(gallery_feat_path, 'rb') as file:
                    gallery_feat = pickle.load(file)
                    if gallery_feat == {}:
                        filename = gallery_feat_path.split("/")[-1]
                        logging.warning(f'{filename} gait feature empty because extracted feature extraction interuptted before or do not have person in it.')
                        continue
            else:
                filename = gallery_feat_path.split("/")[-1]
                logging.warning(f'{filename} did not extracted feature.')
                continue
            '''
            collect all feat from each id in each video and calculate distance
            so each id of each video = an item
            '''
            
            _, all_compare = compare(gallery_feat, probe_feat, mode = 'multi')
            for key, value in all_compare.items():
                item = {
                "probe_feat_path": fix_path(probe_feat_path),
                "gallery_feat_path": fix_path(gallery_feat_path),
                "probe_id" : key.split('-gallery')[0].split(':')[1],
                "gallery_id" : key.split('-gallery')[1].split(':')[1],
                "distance" : value
                }
                item_ls.append(item)
            
            compare_session_save_path = os.path.join(compare_session_folder,session + '.pkl')
            ranking_ls = display_all_distance(item_ls)
            with open (compare_session_save_path, 'wb') as file:
                pickle.dump(ranking_ls, file)
            
    return compare_session_save_path, ranking_ls



def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run(app, host=host_ip, port=int(rec_port_num), reload=False)
    # uvicorn.run("sample_rec:app", host=host_ip, port=int(rec_port_num), reload=True)


if __name__ == "__main__":
    main()


