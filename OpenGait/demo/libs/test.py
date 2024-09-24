
import os 
import sys
from utils_server.api_server import *

sys.path.append(os.path.abspath('.') + "/demo/libs/")
from segment import *
import ast
from fastapi import FastAPI, HTTPException, Form, Request
import uvicorn
import configparser
config = configparser.ConfigParser()
current_script_directory = os.path.dirname(os.path.abspath(__file__))
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
seg_port_num = config['DEFAULT']['seg_port_num'] 
parent_dir = os.path.dirname(current_script_directory)

pickle_path = os.path.join(current_script_directory,"pickle_variables")
pickle_path_seg = os.path.join(pickle_path, 'segment')
save_root = os.path.join(parent_dir, 'output')
sil_save_path = os.path.join(save_root,'GaitSilhouette')

os.makedirs(pickle_path, exist_ok=True)
os.makedirs(pickle_path_seg, exist_ok=True)
os.makedirs(save_root, exist_ok=True)
os.makedirs(sil_save_path, exist_ok=True)
# only folder of cropped image of a single track target 
def segment_no_video(folder_track_path, frame_skip_num):
    print ('gayyyyyy')
    print (folder_track_path)
    frame_rate_segment = frame_skip_num + 1 
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
    
    tid = 1
    sil_pickle_path = os.path.join(pickle_path_seg,save_video_name)
    segment_folder_path = os.path.join(sil_save_path,save_video_name)

    silhouette = seg_no_video(save_video_name, sil_save_path, tid, folder_track_path, frame_rate_segment)
    with open(sil_pickle_path, 'wb') as file:
        pickle.dump(silhouette, file)
    segment_folder_path = Path(segment_folder_path)
    sil_pickle_path = Path(sil_pickle_path)

    res = {
            "status": 1,
            "error_code": None,
            "error_message": None, 
            "result": 
                {
                "segment_folder_path": fix_path(segment_folder_path), 
                'sil_pickle_path': fix_path(sil_pickle_path)
                }
        }    
    print ('Done Segment')
    return res
string = r"C:\Pro\rcs\face\production\251\tracking\Gait_recognition_v2\testing_images\aotrang"
path = (fix_path(string))
print (path)
segment_no_video(path, 4)