import os
import sys
import requests
import json 
import ast

sys.path.append(os.path.abspath('.') + "/demo/libs/")
from utils.api_server import *
import configparser
config = configparser.ConfigParser()
current_script_directory = os.path.dirname(os.path.abspath(__file__))

config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
track_port_num = config['DEFAULT']['track_port_num'] 
seg_port_num = config['DEFAULT']['seg_port_num']
rec_port_num = config['DEFAULT']['rec_port_num']


url_tracking = f'http://{host_ip}:{track_port_num}/tracking'
url_seg = f'http://{host_ip}:{seg_port_num}/segment'
url_rec = f'http://{host_ip}:{rec_port_num}/extract-sil-function'
url_compare_multi = f'http://{host_ip}:{rec_port_num}/compare-feat-multi'
url_compare_single = f'http://{host_ip}:{rec_port_num}/compare-feat-single'
write_result = f'http://{host_ip}:{track_port_num}/write-result'
url_compare_multi_probe_video = f'http://{host_ip}:{rec_port_num}/compare-multi-probe-video'

video_save_folder = os.path.dirname(current_script_directory)
pickle_path = os.path.join(current_script_directory,"pickle_variables")

### only need to change input_video_name (every made folder will follow this name)
### put wanna write result video to same video save folder 
input_video_name = 'huong.mp4'
video_save_folder_name = input_video_name.replace('.mp4','')
folder_name = input_video_name.replace('.mp4','')
video_save_folder = video_save_folder + '/output/OutputVideos/' + video_save_folder_name
folder_path = os.path.join(pickle_path, folder_name)
os.makedirs(folder_path, exist_ok=True)
track_output_pickle = os.path.join(folder_path,"track_output.pickle")
rec_output_pickle = os.path.join(folder_path,"rec_output.pickle")
seg_output_pickle = os.path.join(folder_path,"seg_output.pickle")
final_output_pickle = os.path.join(folder_path,"final_output.pickle")
compare_output_pickle = os.path.join(folder_path,"compare_output.pickle")


def track_service():
        gallery_video_path = os.path.dirname(current_script_directory) + '/output/InputVideos/' + input_video_name
        path_dict = {'gallery_video_path': gallery_video_path, "video_save_folder": video_save_folder}
        track_response = requests.post(url_tracking, json=path_dict)
        pickle_response(track_response, track_output_pickle)
        print ('saved tracking result in path (to send to segment server): ', track_output_pickle)


def seg_service():
        with open(track_output_pickle, 'rb') as file:
            # Deserialize and retrieve the variable from the file
            track_response_json = pickle.load(file)
            track_response_json = keys2int(track_response_json, 'gallery_track_result')
            # track_response_json = keys2int(track_response_json, 'probe1_track_result')
            
        response = requests.post(url_seg, json=track_response_json)
        pickle_response(response, seg_output_pickle)
        print ('saved segment result in path (to send to rec server): ', seg_output_pickle)

    
def rec_service():
        with open(seg_output_pickle, 'rb') as file:
            # Deserialize and retrieve the variable from the file
            seg_response_json = pickle.load(file)
            seg_response_json["rec_output_pickle"] = rec_output_pickle

        response = requests.post(url_rec, json=seg_response_json)
        print ('saved rec result in path: ', rec_output_pickle)


def compare_multi_probes(gallery_vid_name, list_probe_vid_name):
    '''
    given lots of embedding in 1 vid , find the most similar embeds in those embed 
    find distance , lets try multi first 
    
    
    after then given an embedding store , find it 
    each vid have embedding store 
    
    not finding in embed store, it is find embed in the vid 
    
    
    so given multiple probes vid embed extracted, find the most similar embed in those
    one is gallery 
    many is probe 
    '''         
    
    count = 0 
    list_probe_feat_path = []
    list_distance_file_name = []
    gallery_name = gallery_vid_name.replace(".mp4", "")
    for probe_vid_name in list_probe_vid_name:
        probe_vid_name = probe_vid_name.replace(".mp4", "")
        probe_vid_feat_path = os.path.join(pickle_path, probe_vid_name) + "/rec_output.pickle"
        list_probe_feat_path.append(probe_vid_feat_path)
        distance_file_name = gallery_name + '_' + probe_vid_name
        count += 1 
        list_distance_file_name.append(distance_file_name + str(count))
        
    gallery_feat_path = os.path.join(pickle_path, gallery_name) + "/rec_output.pickle"
    input_compare_json = {"gallery_feat_path": gallery_feat_path,
                          "list_probe_feat_path": list_probe_feat_path, 
                          "video_save_folder": video_save_folder, 
                          "list_distance_file_name": list_distance_file_name}

    response = requests.post(url_compare_multi_probe_video, json=input_compare_json)
    pickle_response(response, compare_output_pickle)

def write_result_video():
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
            


if __name__ == "__main__":
    print ('start tracking')
    track_service()
    print ('done tracking')
    print ('start segment')
    seg_service()
    print ('done segment')
    print ('start recognition')
    rec_service()
    print ('done recognition')
    # print ('start compare')
    # compare_multi_probes(gallery_vid_name = 'kien7.mp4', probe_vid_name = 'manh.mp4')
    # print ('done compare')
    
    
    
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
    
    
