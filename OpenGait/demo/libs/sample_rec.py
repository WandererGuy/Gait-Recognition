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
import torch
import configparser
import logging 
from tqdm import tqdm
current_script_directory = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
rec_port_num = config['DEFAULT']['rec_port_num'] 

save_root = './demo/output/'
gait_feat_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
result_distance_folder = gait_feat_folder + '/output/ResultDistance/'
gait_feat_folder = gait_feat_folder + '/output/GaitFeatures/'
app = FastAPI()



def get_gait_feat(feat_dict:dict):
    all_embs = {}
    for key, value in feat_dict.items():
        path = os.path.join(gait_feat_folder,key,value,'undefined','undefined.pkl')
        embs = pickle.load(file = open(path, 'rb'))
        all_embs[f'{key}_{value}'] = embs
    return all_embs   

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
    rec_output_pickle = data["rec_output_pickle"]
    data = data["output"]
    data = json.loads(data)
    silhouette = data["silhouette"]
    if silhouette != []:
        # recognise
        if not os.path.exists(rec_output_pickle):
            video_feat = extract_sil(silhouette, save_root+'/GaitFeatures/')
            print ('done recognise')
            with open(rec_output_pickle, 'wb') as file:
                pickle.dump(video_feat, file)
        return {"message": "success"}
    else: 
        return {"message": "sil result is empty already"} 

@app.post("/compare-multi-gallery-video")
async def compare_multi_gallery_video(request: Request):
    data = await request.json()
    session = data["session"]
    list_gallery_feat_path = data["list_gallery_feat_path"]
    probe_feat_path = data["probe_feat_path"]
    additional_info_ls = data["additional_info_ls"]
    full_probe = data["full_probe"]
    if not full_probe:
        probe_id = data["probe_id"]
        with open(probe_feat_path, 'rb') as file:
            probe_feat = pickle.load(file)
            probe_feat = {'probe':[{probe_id: {'undefined': probe_feat }}]}  
    else:
        with open(probe_feat_path, 'rb') as file:
            probe_feat = pickle.load(file)
    item_ls = []
    print (list_gallery_feat_path)
    for index, gallery_feat_path in enumerate(tqdm(list_gallery_feat_path)):
            if os.path.exists(gallery_feat_path):  
                with open(gallery_feat_path, 'rb') as file:
                    gallery_feat = pickle.load(file)
                    if gallery_feat == {}:
                        filename = gallery_feat_path.split("/")[-1]
                        logging.warning(f'{filename} gait feature empty because extracted feature extraction interuptted before or do not have person in it.')
                        print ('gayyyyyy')
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
            os.makedirs(os.path.join(result_distance_folder,session), exist_ok=True)
            for key, value in all_compare.items():
                item = {
                "session": session, 
                "probe_name": additional_info_ls[index]["probe_name"],
                "gallery_name": additional_info_ls[index]["gallery_name"], 
                "gallery_duplicate_name_id": additional_info_ls[index]["gallery_duplicate_name_id"],
                "probe_id" : key.split('-gallery')[0].split(':')[1],
                "gallery_id" : key.split('-gallery')[1].split(':')[1],
                "distance" : value
                }
                item_ls.append(item)
            save_path = os.path.join(result_distance_folder,str(session) + '.pkl')
            pickle.dump(item_ls, open(save_path, "wb"))
            # write_distance_file = os.path.join(result_distance_folder,session,str(list_distance_file_name[index] + '.txt'))
            # with open(write_distance_file, 'w') as file:
            #     for key, value in all_compare.items():
            #         file.write(key + ' : ' + str(value) + '\n')
            #     print ('result distance all videos written in ' + write_distance_file)


    return {'message': 'success, result distance all videos written in ' , 'path': save_path}


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

def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_rec:app", host=host_ip, port=int(rec_port_num), reload=True)

if __name__ == "__main__":
    main()