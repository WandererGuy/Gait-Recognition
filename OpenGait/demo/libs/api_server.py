import os
import sys
import requests
import json 
import ast
from tqdm import tqdm
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from utils.api_server import *
import configparser
config = configparser.ConfigParser()
import logging 

current_script_directory = os.path.dirname(os.path.abspath(__file__))

config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
track_port_num = config['DEFAULT']['track_port_num'] 
seg_port_num = config['DEFAULT']['seg_port_num']
rec_port_num = config['DEFAULT']['rec_port_num']


url_tracking = f'http://{host_ip}:{track_port_num}/tracking'
url_seg = f'http://{host_ip}:{seg_port_num}/segment'
url_seg_no_video = f'http://{host_ip}:{seg_port_num}/segment-no-video'
url_rec = f'http://{host_ip}:{rec_port_num}/extract-sil-function'
url_compare_multi = f'http://{host_ip}:{rec_port_num}/compare-feat-multi'
url_compare_single = f'http://{host_ip}:{rec_port_num}/compare-feat-single'
write_result = f'http://{host_ip}:{track_port_num}/write-result'
url_compare_multi_gallery_video = f'http://{host_ip}:{rec_port_num}/compare-multi-gallery-video'

parent_folder = os.path.dirname(current_script_directory)
pickle_path = os.path.join(current_script_directory,"pickle_variables")
gait_feature_folder = parent_folder + '/output/GaitFeatures/'
track_video_save_folder = parent_folder + '/output/OutputVideos/' 

def create_folders(input_video_name):
        video_save_folder_name = input_video_name.replace('.mp4','')
        folder_name = input_video_name.replace('.mp4','')
        folder_path = os.path.join(pickle_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        track_output_pickle = os.path.join(folder_path,"track_output.pickle")
        rec_output_pickle = os.path.join(folder_path,"rec_output.pickle")
        seg_output_pickle = os.path.join(folder_path,"seg_output.pickle")
        final_output_pickle = os.path.join(folder_path,"final_output.pickle")
        compare_output_pickle = os.path.join(folder_path,"compare_output.pickle")
        data = [video_save_folder_name, folder_name, folder_path, track_output_pickle, seg_output_pickle, rec_output_pickle, final_output_pickle, compare_output_pickle]
        return data
def track_service(data, input_video_name):
        video_save_folder_name, folder_name, folder_path, track_output_pickle, seg_output_pickle, rec_output_pickle, final_output_pickle, compare_output_pickle = data
        video_path = parent_folder + '/output/InputVideos/' + input_video_name
        path_dict = {'video_path':video_path, "video_save_folder": os.path.join(track_video_save_folder, video_save_folder_name)}
        track_response = requests.post(url_tracking, json=path_dict)
        pickle_response(track_response, track_output_pickle)
        print ('saved tracking result in path (to send to segment server): ', track_output_pickle)


def seg_service(data):
        video_save_folder_name, folder_name, folder_path, track_output_pickle, seg_output_pickle, rec_output_pickle, final_output_pickle, compare_output_pickle = data
        with open(track_output_pickle, 'rb') as file:
            track_response_json = pickle.load(file)
            track_response_json = keys2int(track_response_json, 'track_result')
            
        response = requests.post(url_seg, json=track_response_json)
        pickle_response(response, seg_output_pickle)
        if response.status_code == 200:
            print ('saved segment result in path (to send to rec server): ', seg_output_pickle)
        else:
            print("Request failed with status code: ", response.status_code)
def seg_service_no_video(data, folder_track_path, choose_video_name = "random", tid = 1):
        video_save_folder_name, folder_name, folder_path, track_output_pickle, seg_output_pickle, rec_output_pickle, final_output_pickle, compare_output_pickle = data
        track_response_json = { "choose_video_name": choose_video_name,
                                "tid": tid,
                                "folder_track_path": folder_track_path,
                                 }
        response = requests.post(url_seg_no_video, json=track_response_json)
        pickle_response(response, seg_output_pickle)
        if response.status_code == 200:
            print ('saved segment result in path (to send to rec server): ', seg_output_pickle)
        else:
            print("Request failed with status code: ", response.status_code)


    
def rec_service(data):
        video_save_folder_name, folder_name, folder_path, track_output_pickle, seg_output_pickle, rec_output_pickle, final_output_pickle, compare_output_pickle = data
        with open(seg_output_pickle, 'rb') as file:
            # Deserialize and retrieve the variable from the file
            seg_response_json = pickle.load(file)
            seg_response_json["rec_output_pickle"] = rec_output_pickle

        response = requests.post(url_rec, json=seg_response_json)
        json_response = response.json()
        if json_response["message"] == "success":
            print ('saved rec result in path: ', rec_output_pickle)
        else:
            print("Request failed: ", json_response["message"])

def compare_multi_gallery(compare_session, probe_vid_name, list_gallery_vid_name, full_probe=True, probe_id = None):
    list_gallery_feat_path = []
    additional_info_ls = []
    probe_name = probe_vid_name.replace(".mp4", "")
    for gallery_vid_name in list_gallery_vid_name:
        gallery_vid_name = gallery_vid_name.replace(".mp4", "")
        gallery_vid_feat_path = os.path.join(pickle_path, gallery_vid_name) + "/rec_output.pickle"
        list_gallery_feat_path.append(gallery_vid_feat_path)
        count = check_name_in_list(list_gallery_feat_path, gallery_vid_feat_path) 
        additional = {'probe_name': probe_name, 'gallery_name': gallery_vid_name, 'gallery_duplicate_name_id': count}
        additional_info_ls.append(additional)
    
    if full_probe:
            probe_feat_path = os.path.join(pickle_path, probe_name) + "/rec_output.pickle"
    else:
            probe_feat_path = os.path.join(gait_feature_folder, probe_name, probe_id, 'undefined', 'undefined.pkl')
    input_compare_json = {"probe_feat_path": probe_feat_path,
                          "list_gallery_feat_path": list_gallery_feat_path, 
                          "additional_info_ls": additional_info_ls, 
                          "full_probe": full_probe,
                          "probe_id": probe_id, 
                          "session": compare_session}

    response = requests.post(url_compare_multi_gallery_video, json=input_compare_json)
    response_json =  json.loads(response.text)
    return response_json['path']

def write_result_video(data):
        ### put wanna write result video to same video save folder 
        video_save_folder_name, folder_name, folder_path, track_output_pickle, seg_output_pickle, rec_output_pickle, final_output_pickle, compare_output_pickle = data
        with open (compare_output_pickle, 'rb') as file:
            # Deserialize and retrieve the variable from the file
            gallery_probe1_result = pickle.load(file)

            gallery_probe1_result = gallery_probe1_result['output']["gallery_probe1_result"]     
            probe1_video_path = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/OutputVideos/1/kien7.mp4"
            video_save_folder = video_save_folder                     
        loaded_data = None
        input = {
            "gallery_probe1_result": gallery_probe1_result,
            "probe1_video_path": probe1_video_path,
            "video_save_folder": video_save_folder
            }
        response = requests.post(write_result, json=input)
        pickle_response(response, final_output_pickle)
        final_resopnse = response.json()
        print (final_resopnse)
             
def change_pickle_path(saved_pickle_folder_name):
    global pickle_path 
    pickle_path = os.path.join(pickle_path, saved_pickle_folder_name)

if __name__ == "__main__":
    # saved_pickle_folder_name = '3'
    # change_pickle_path(saved_pickle_folder_name)
    # input_video_name='mai.mp4'    
    # data = create_folders(input_video_name)
    # print ('start tracking')
    # track_service(data, input_video_name)
    # print ('done tracking')
    # print ('start segment')
    # seg_service(data)
    # print ('done segment')
    # print ('start recognition')
    # rec_service(data)
    # print ('done recognition')
    
    
    
    ##### only start compare once all rec is over , or else , rec is skipped somehow
    saved_pickle_folder_name = '3'
    change_pickle_path(saved_pickle_folder_name)

    print ('start compare')
    full_probe = False
    compare_session = '3'
    probe_id = '001'
    probe_vid_name = 'kien7.mp4'

    list_gallery_vid_name = []
    for filename in sorted(os.listdir(pickle_path)):
        list_gallery_vid_name.append(filename)
    save_path = compare_multi_gallery(
                         compare_session = compare_session,
                         probe_vid_name = probe_vid_name, 
                         list_gallery_vid_name = list_gallery_vid_name, 
                         full_probe=full_probe, 
                         probe_id = probe_id,
                         )
    compare_result = pickle.load(open(save_path, 'rb'))
    ranking_ls = display_all_distance(compare_result)

    # print ('=======Third minimum distance object=======')
    # print (ranking_ls[2])
    # print ('=======Second minimum distance object=======')
    # print (ranking_ls[1])
    # print ('=======Most minimum distance object=======')
    # print (ranking_ls[0])
    
    
    for item in ranking_ls:
        print (item)
    print ('done compare')



########## COLLECT EMBEDDING FOR EVALUATE REC MODEL ################ 
# MAKING 100 EMBEDS FROM MULTIPLE VIDEOS TO CREATE 100 GALLERY EMBEDS
# THEN WITH 1 PROBE , WILL SEE WITH 1 PROBE ID , WHICH GALLERY EMBED IT WILL MATCH 
# GALLERY IS MATERIALS POOL , SO THAT PROBE CAN PICK FROM GALLERY EMBEDS
    
    # ##### collect embedding from tracked frames from dataset 
    # saved_pickle_folder_name = '3'
    # change_pickle_path(saved_pickle_folder_name)

    # main_folder = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/mars/bbox_test/bbox_test/'
    # count = 0 
    # for index, filename in enumerate(tqdm(sorted(os.listdir(main_folder)))):
    #         if count == 30:
    #             break
    #         folder_track_path = main_folder + filename
    #         if len(os.listdir(folder_track_path)) > 150:
    #             continue
    #         choose_video_name = folder_track_path.split('/')[-2] + '_' + folder_track_path.split('/')[-1]
    #         data = create_folders(input_video_name=choose_video_name)
            # print ('start segment')
            # tid = 1 
            # seg_service_no_video(data, folder_track_path, choose_video_name, tid)
            # print ('done segment')
            # print ('PROCESSING VIDEO: ', filename)

            # print ('start recognition')
            # rec_service(data)
            # print ('done recognition')
            # count += 1 

    
    '''
    get many video to get 100 embeddings 
    add kien embedding to that 
    all this belongs to probe 
    
    i have a gallery video of kien with known kien id 
    i then use kien id to get distance with other embedding 
    i will plot those , to see which top 3 is 
    if exist kien , i success
    time to collect embedding from videos 
    
    
    to collect 
    first i can get from tracking dataset 
    '''
    
    
