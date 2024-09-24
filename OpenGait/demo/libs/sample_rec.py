import os
import sys
from utils_server.api_server import *
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from recognise import *
import requests
import json 
from fastapi import FastAPI, HTTPException, Form, Request
import uvicorn
import torch
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

app = FastAPI()
# gait_feature_folder = parent_folder + '/output/GaitFeatures/'

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
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device being used: {device}")
    uvicorn.run("sample_rec:app", host=host_ip, port=int(rec_port_num), reload=True)

if __name__ == "__main__":
    main()
















# @app.post("/compare-feat-from-probe-video")
# async def compare_feat_from_probe_video(full_probe: bool = Form(...), 
#                                         compare_session: str = Form(...), 
#                                         probe_id: str = Form("001"), 
#                                         probe_feat_path: str = Form(...), 
#                                         list_gallery_feat_path: List[str]  = Form(...)):

#     # ls = []
#     # for filename in list_gallery_vid_name:
#     #     ls.append(os.path.join(pickle_path, filename))
#     save_path = compare_multi_gallery_modified(
#                          compare_session = compare_session,
#                          probe_feat_path = probe_feat_path, 
#                          list_gallery_feat_path = list_gallery_feat_path, 
#                          full_probe=full_probe, 
#                          probe_id = probe_id,
#                          )
#     compare_result = pickle.load(open(save_path, 'rb'))
#     ranking_ls = display_all_distance(compare_result)

#     # print ('=======Third minimum distance object=======')
#     # print (ranking_ls[2])
#     # print ('=======Second minimum distance object=======')
#     # print (ranking_ls[1])
#     # print ('=======Most minimum distance object=======')
#     # print (ranking_ls[0])
    
    
#     for item in ranking_ls:
#         print (item)
#     print ('done compare')

#     return {"message": "success", "ranking_ls": ranking_ls}


# current_script_directory = os.path.dirname(os.path.abspath(__file__))
# parent_folder = os.path.dirname(current_script_directory)
# pickle_path = os.path.join(current_script_directory,"pickle_variables")
# gait_feature_folder = parent_folder + '/output/GaitFeatures/'
# url_compare_multi_gallery_video = f'http://{host_ip}:{rec_port_num}/compare-multi-gallery-video'


# def compare_multi_gallery_modified(compare_session, probe_feat_path, list_gallery_feat_path, full_probe=True, probe_id = None):
#     if full_probe:
#             probe_feat_path = probe_feat_path
#     else:
#             probe_name = Path(probe_feat_path).name
#             probe_feat_path = os.path.join(gait_feature_folder, probe_name, probe_id, 'undefined', 'undefined.pkl')
#     input_compare_json = {"probe_feat_path": probe_feat_path,
#                           "list_gallery_feat_path": list_gallery_feat_path, 
#                           "full_probe": full_probe,"probe_id": probe_id, 
#                           "session": compare_session}
#     response_json = compare_multi_gallery_video(input_compare_json)
#     return response_json['path']


# def compare_multi_gallery_video(data: dict):
#     session = data["session"]
#     list_gallery_feat_path = data["list_gallery_feat_path"]
#     probe_feat_path = data["probe_feat_path"]
#     full_probe = data["full_probe"]
#     if not full_probe:
#         probe_id = data["probe_id"]
#         with open(probe_feat_path, 'rb') as file:
#             probe_feat = pickle.load(file)
#             tmp = Path(probe_feat_path).name
#             probe_feat = {tmp:[{probe_id: {'undefined': probe_feat }}]}  
#     else:
#         with open(probe_feat_path, 'rb') as file:
#             probe_feat = pickle.load(file)
#     item_ls = []
#     for index, gallery_feat_path in enumerate(tqdm(list_gallery_feat_path)):
#             if os.path.exists(gallery_feat_path):  
#                 with open(gallery_feat_path, 'rb') as file:
#                     gallery_feat = pickle.load(file)
#                     if gallery_feat == {}:
#                         filename = gallery_feat_path.split("/")[-1]
#                         logging.warning(f'{filename} gait feature empty because extracted feature extraction interuptted before or do not have person in it.')
#                         continue
#             else:
#                 filename = gallery_feat_path.split("/")[-1]
#                 logging.warning(f'{filename} did not extracted feature.')
#                 continue
#             '''
#             collect all feat from each id in each video and calculate distance
#             so each id of each video = an item
#             '''
            
#             _, all_compare = compare(gallery_feat, probe_feat, mode = 'multi')
#             os.makedirs(os.path.join(result_distance_folder,session), exist_ok=True)
#             for key, value in all_compare.items():
#                 item = {
#                 "session": session, 
#                 "probe_feat_path": probe_feat_path,
#                 "gallery_feat_path": gallery_feat_path,
#                 "probe_id" : key.split('-gallery')[0].split(':')[1],
#                 "gallery_id" : key.split('-gallery')[1].split(':')[1],
#                 "distance" : value
#                 }
#                 item_ls.append(item)
#             save_path = os.path.join(result_distance_folder,str(session) + '.pkl')
#             pickle.dump(item_ls, open(save_path, "wb"))
#             # write_distance_file = os.path.join(result_distance_folder,session,str(list_distance_file_name[index] + '.txt'))
#             # with open(write_distance_file, 'w') as file:
#             #     for key, value in all_compare.items():
#             #         file.write(key + ' : ' + str(value) + '\n')
#             #     print ('result distance all videos written in ' + write_distance_file)


#     return {'message': 'success, result distance all videos written in ' , 'path': save_path}


















# @app.post("/compare-server")
# async def compare_server(full_probe, compare_session, probe_id, probe_vid_name, list_gallery_vid_name):

#     # ls = []
#     # for filename in list_gallery_vid_name:
#     #     ls.append(os.path.join(pickle_path, filename))
#     ls = list_gallery_vid_name
#     save_path = compare_multi_gallery_modified(
#                          compare_session = compare_session,
#                          probe_vid_name = probe_vid_name, 
#                          list_gallery_vid_name = ls, 
#                          full_probe=full_probe, 
#                          probe_id = probe_id,
#                          )
#     compare_result = pickle.load(open(save_path, 'rb'))
#     ranking_ls = display_all_distance(compare_result)

#     # print ('=======Third minimum distance object=======')
#     # print (ranking_ls[2])
#     # print ('=======Second minimum distance object=======')
#     # print (ranking_ls[1])
#     # print ('=======Most minimum distance object=======')
#     # print (ranking_ls[0])
    
    
#     for item in ranking_ls:
#         print (item)
#     print ('done compare')

#     return {"message": "success", "ranking_ls": ranking_ls}

          
# current_script_directory = os.path.dirname(os.path.abspath(__file__))
# parent_folder = os.path.dirname(current_script_directory)
# pickle_path = os.path.join(current_script_directory,"pickle_variables")
# gait_feature_folder = parent_folder + '/output/GaitFeatures/'
# url_compare_multi_gallery_video = f'http://{host_ip}:{rec_port_num}/compare-multi-gallery-video'

          
# def compare_multi_gallery_modified(compare_session, probe_vid_name, list_gallery_vid_name, full_probe=True, probe_id = None):
#     list_gallery_feat_path = []
#     additional_info_ls = []
#     probe_name = probe_vid_name.replace(".mp4", "")
#     for gallery_vid_name in list_gallery_vid_name:
#         gallery_vid_name = gallery_vid_name.replace(".mp4", "")
#         gallery_vid_feat_path = os.path.join(pickle_path, gallery_vid_name) + "/rec_output.pkl"
#         list_gallery_feat_path.append(gallery_vid_feat_path)
#         count = check_name_in_list(list_gallery_feat_path, gallery_vid_feat_path) 
#         additional = {'probe_name': probe_name, 'gallery_name': gallery_vid_name, 'gallery_duplicate_name_id': count}
#         additional_info_ls.append(additional)
    
#     if full_probe:
#             probe_feat_path = os.path.join(pickle_path, probe_name) + "/rec_output.pkl"
#     else:
#             probe_feat_path = os.path.join(gait_feature_folder, probe_name, probe_id, 'undefined', 'undefined.pkl')
#     input_compare_json = {"probe_feat_path": probe_feat_path,
#                           "list_gallery_feat_path": list_gallery_feat_path, 
#                           "additional_info_ls": additional_info_ls, 
#                           "full_probe": full_probe,
#                           "probe_id": probe_id, 
#                           "session": compare_session}

#     response = requests.post(url_compare_multi_gallery_video, json=input_compare_json)
#     response_json =  json.loads(response.text)
#     return response_json['path']




# @app.post("/compare-multi-gallery-video")
# async def compare_multi_gallery_video(request: Request):
#     data = await request.json()
#     session = data["session"]
#     list_gallery_feat_path = data["list_gallery_feat_path"]
#     probe_feat_path = data["probe_feat_path"]
#     additional_info_ls = data["additional_info_ls"]
#     full_probe = data["full_probe"]
#     if not full_probe:
#         probe_id = data["probe_id"]
#         with open(probe_feat_path, 'rb') as file:
#             probe_feat = pickle.load(file)
#             probe_feat = {'probe':[{probe_id: {'undefined': probe_feat }}]}  
#     else:
#         with open(probe_feat_path, 'rb') as file:
#             probe_feat = pickle.load(file)
#     item_ls = []
#     print (list_gallery_feat_path)
#     for index, gallery_feat_path in enumerate(tqdm(list_gallery_feat_path)):
#             if os.path.exists(gallery_feat_path):  
#                 with open(gallery_feat_path, 'rb') as file:
#                     gallery_feat = pickle.load(file)
#                     if gallery_feat == {}:
#                         filename = gallery_feat_path.split("/")[-1]
#                         logging.warning(f'{filename} gait feature empty because extracted feature extraction interuptted before or do not have person in it.')
#                         continue
#             else:
#                 filename = gallery_feat_path.split("/")[-1]
#                 logging.warning(f'{filename} did not extracted feature.')
#                 continue
#             '''
#             collect all feat from each id in each video and calculate distance
#             so each id of each video = an item
#             '''
            
#             _, all_compare = compare(gallery_feat, probe_feat, mode = 'multi')
#             os.makedirs(os.path.join(result_distance_folder,session), exist_ok=True)
#             for key, value in all_compare.items():
#                 item = {
#                 "session": session, 
#                 "probe_name": additional_info_ls[index]["probe_name"],
#                 "gallery_name": additional_info_ls[index]["gallery_name"], 
#                 "gallery_duplicate_name_id": additional_info_ls[index]["gallery_duplicate_name_id"],
#                 "probe_id" : key.split('-gallery')[0].split(':')[1],
#                 "gallery_id" : key.split('-gallery')[1].split(':')[1],
#                 "distance" : value
#                 }
#                 item_ls.append(item)
#             save_path = os.path.join(result_distance_folder,str(session) + '.pkl')
#             pickle.dump(item_ls, open(save_path, "wb"))
#             # write_distance_file = os.path.join(result_distance_folder,session,str(list_distance_file_name[index] + '.txt'))
#             # with open(write_distance_file, 'w') as file:
#             #     for key, value in all_compare.items():
#             #         file.write(key + ' : ' + str(value) + '\n')
#             #     print ('result distance all videos written in ' + write_distance_file)


#     return {'message': 'success, result distance all videos written in ' , 'path': save_path}


# @app.post("/compare-feats")
# async def compare_feats(request: Request):
#     '''
#     with specific embs vs specific embs
#     write distance into txt
#     '''

#     data = await request.json()
#     gallery_feat_dict = data["gallery_feat_dict"]
#     # {video_name:gait_id}
#     probe1_feat_dict = data["probe1_feat_dict"]
#     # {video_name:gait_id}
#     gallery_feats = get_gait_feat(gallery_feat_dict)
#     probe1_feats = get_gait_feat(probe1_feat_dict)
#     with open (result_distance_folder + 'distance.txt', 'w') as file:
#         for probe_key, probe_value in probe1_feats.items():
#             for galler_key, gallery_value in gallery_feats.items():
#                 distance = computedistence(probe_value, gallery_value)
#                 file.write (f'{probe_key} vs {galler_key}: {distance}')
    
    
# @app.post("/compare-multi-probe-video")
# async def compare_multi_probe_video(request: Request):
#     data = await request.json()
#     session = data["session"]
#     list_probe_feat_path = data["list_probe_feat_path"]
#     gallery_feat_path = data["gallery_feat_path"]
#     origin_info_ls = data["origin_info_ls"]
#     full_gallery = data["full_gallery"]
#     if not full_gallery:
#         gallery_id = data["gallery_id"]
#         with open(gallery_feat_path, 'rb') as file:
#             gallery_feat = pickle.load(file)
#             gallery_feat = {'gallery':[{gallery_id: {'undefined': gallery_feat }}]}  
#     else:
#         with open(gallery_feat_path, 'rb') as file:
#             gallery_feat = pickle.load(file)
    
#     for index, probe1_feat_path in enumerate(list_probe_feat_path):
#             with open(probe1_feat_path, 'rb') as file:
#                 probe1_feat = pickle.load(file)
#             _, all_compare = compare(probe1_feat, gallery_feat, mode = 'multi')
#             os.makedirs(os.path.join(result_distance_folder,session), exist_ok=True)
#             item_ls = []
#             for key, value in all_compare.items():
#                 item = {
#                 "session": session, 
#                 "gallery_name": origin_info_ls[index]["gallery_name"],
#                 "probe_name": origin_info_ls[index]["probe_name"], 
#                 "probe_duplicate_name_id": origin_info_ls[index]["probe_duplicate_name_id"],
#                 "gallery_id" : key.split('-probe')[0].split(':')[1],
#                 "probe_id" : key.split('-probe')[1].split(':')[1],
#                 "distance" : value
#                 }
#                 item_ls.append(item)
#             save_path = os.path.join(result_distance_folder,str(session) + '.pkl')
#             pickle.dump(item_ls, open(save_path, "wb"))
#             # write_distance_file = os.path.join(result_distance_folder,session,str(list_distance_file_name[index] + '.txt'))
#             # with open(write_distance_file, 'w') as file:
#             #     for key, value in all_compare.items():
#             #         file.write(key + ' : ' + str(value) + '\n')
#             #     print ('result distance all videos written in ' + write_distance_file)


#     return {'message': 'success, result distance all videos written in ' , 'path': save_path}






# @app.post("/compare-feat-multi")
# async def compare_feat_multi(request: Request):
#     data = await request.json()
#     video_save_folder = data["video_save_folder"] 
#     # Get the value associated with the 'result' key

#     probe1_feat_path = data["probe1_feat_path"]
#     gallery_feat_path = data["gallery_feat_path"]
#     distance_file_name = data["distance_file_name"]
    
    
#     with open(gallery_feat_path, 'rb') as file:
#         # Deserialize and retrieve the variable from the file
#         gallery_feat = pickle.load(file)
#     if 'video_save_folder' in gallery_feat:
#         del gallery_feat['video_save_folder']

#     with open(probe1_feat_path, 'rb') as file:
#         # Deserialize and retrieve the variable from the file
#         probe1_feat = pickle.load(file)
#     if 'video_save_folder' in probe1_feat:

#         del probe1_feat['video_save_folder']
#     gallery_probe1_result, all_compare = compare(probe1_feat, gallery_feat, mode = 'multi')
#     # gallery_probe2_result = compare(probe2_feat, gallery_feat)
#     # gallery_probe3_result = compare(probe3_feat, gallery_feat)
#     # gallery_probe4_result = compare(probe4_feat, gallery_feat)

#     write_distance_file = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/ResultDistance'
#     write_distance_file = write_distance_file + '/' + distance_file_name + '.txt'
#     with open(write_distance_file, 'w') as file:
#         for key, value in all_compare.items():
#             file.write(key + ' : ' + str(value) + '\n')
#     print ('result distance written in ' + write_distance_file)
#     output = {
#         "gallery_probe1_result": gallery_probe1_result,
#         # "gallery_probe2_result": gallery_probe2_result,
#         # "gallery_probe3_result": gallery_probe3_result,
#         # "gallery_probe4_result": gallery_probe4_result,
#         "video_save_folder": video_save_folder
#     }


#     return {"output": output}

# @app.post("/compare-feat-single")
# async def compare_feat_single(request: Request):
#     data = await request.json()
#     id = data["id"]
#     video_save_folder = data["video_save_folder"] 
#     # Get the value associated with the 'result' key
#     mode = data["mode"]
#     probe1_feat_path = data["probe1_feat_path"]
#     gallery_feat_path = data["gallery_feat_path"]

#     with open(probe1_feat_path, 'rb') as file:
#         # Deserialize and retrieve the variable from the file
#         probe1_feat = pickle.load(file)
#     with open(gallery_feat_path, 'rb') as file:
#         # Deserialize and retrieve the variable from the file
#         gallery_feat = pickle.load(file)

#         target_feat = {'gallery':[{id: {'undefined': gallery_feat }}]}  

#     if 'video_save_folder' in probe1_feat:
#         del probe1_feat['video_save_folder']
        
#     gallery_probe1_result = compare(probe1_feat, target_feat, mode = mode)
#     # gallery_probe2_result = compare(probe2_feat, gallery_feat)
#     # gallery_probe3_result = compare(probe3_feat, gallery_feat)
#     # gallery_probe4_result = compare(probe4_feat, gallery_feat)

#     output = {
#         "gallery_probe1_result": gallery_probe1_result,
#         # "gallery_probe2_result": gallery_probe2_result,
#         # "gallery_probe3_result": gallery_probe3_result,
#         # "gallery_probe4_result": gallery_probe4_result,
#         "video_save_folder": video_save_folder
#     }


#     return {"output": output}        

