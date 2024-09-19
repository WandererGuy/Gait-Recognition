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


app = FastAPI()
    

@app.post("/extract-segment-folder") 
# already segment before , have segment folder
# or select out a segement sequence into a folder 
async def extract_segment_folder(segment_folder_path: str = Form(...)):
        segment_folder_path = fix_path(segment_folder_path)
        silhouette = getsil_modified(segment_folder_path)
        save_video_name = Path(segment_folder_path).name
        sil_pickle_path = os.path.join(pickle_path_seg,save_video_name)
        with open(sil_pickle_path, 'wb') as file:
            pickle.dump(silhouette, file)

        segment_folder_path = fix_path(segment_folder_path)
        sil_pickle_path = fix_path(sil_pickle_path)

        res = {
            "status": 1,
            "error_code": None,
            "error_message": None, 
            "result": 
                {
                "segment_folder_path": segment_folder_path, 
                'sil_pickle_path': sil_pickle_path
                }
        }
        print ('Done Segment')
        return res
    


@app.post("/segment-no-video") 
# dont have video
# only folder of cropped image of a single track target 
async def segment_no_video(folder_track_path: str = Form(...), frame_skip_num: int = Form(...)):
    folder_track_path = fix_path(folder_track_path)
    frame_rate_segment = frame_skip_num + 1 
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
    
    tid = 1
    sil_pickle_path = os.path.join(pickle_path_seg,save_video_name)
    segment_folder_path = os.path.join(sil_save_path,save_video_name)

    silhouette = seg_no_video(save_video_name, sil_save_path, tid, folder_track_path, frame_rate_segment)
    with open(sil_pickle_path, 'wb') as file:
        pickle.dump(silhouette, file)
    segment_folder_path = fix_path(segment_folder_path)
    sil_pickle_path = fix_path(sil_pickle_path)

    res = {
            "status": 1,
            "error_code": None,
            "error_message": None, 
            "result": 
                {
                "segment_folder_path": segment_folder_path, 
                'sil_pickle_path': sil_pickle_path
                }
        }    
    print ('Done Segment')
    return res


@app.post("/segment-first-frame") # for init stream folder first image  
# init destination folder 
async def segment_first_frame(image_path: str = Form(...)):
    image_path = fix_path(image_path)
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)

    tid = 1
    # sil_pickle_path = os.path.join(pickle_path_seg,save_video_name)
    segment_folder_path = os.path.join(sil_save_path,save_video_name)
    image_name = seg_single_frame(save_video_name, sil_save_path, tid, image_path, frame_id = 1)
    segment_folder_path = fix_path(segment_folder_path)
    # sil_pickle_path = fix_path(sil_pickle_path)
    image_path = os.path.join(segment_folder_path, image_name)
    image_path = fix_path(image_path)
    res = {
            "status": 1,
            "error_code": None,
            "error_message": None, 
            "result": 
                {
                "segment_folder_path": segment_folder_path, 
                "image_path": image_path,
                }
        }    
    print ('Done Segment')
    return res



@app.post("/segment-adding-frame") # for adding segment to stream folder  
async def segment_adding_frame(image_path: str = Form(...), 
                               segment_folder_path: str = Form(...),
                               frame_id: int = Form(...)):
    image_path = fix_path(image_path)
    save_video_name = Path(segment_folder_path).name
    
    tid = 1
    # sil_pickle_path = os.path.join(pickle_path_seg,save_video_name)
    segment_folder_path = os.path.join(sil_save_path,save_video_name)
    image_name = seg_single_frame(save_video_name, sil_save_path, tid, image_path, frame_id)
    segment_folder_path = fix_path(segment_folder_path)
    # sil_pickle_path = fix_path(sil_pickle_path)
    image_path = os.path.join(segment_folder_path, image_name)
    image_path = fix_path(image_path)

    res = {
            "status": 1,
            "error_code": None,
            "error_message": None, 
            "result": 
                {
                    "image_path": image_path
                }
        }    
    print ('Done Segment')
    return res

# @app.post("/segment-video") 
# # have track result , have video
# async def segment_video(video_path: str = Form(...), track_pickle_path: str = Form(...), frame_skip_num: int = Form(...)):
#     video_path = fix_path(video_path)
#     track_pickle_path = fix_path(track_pickle_path)
#     frame_rate_segment = frame_skip_num + 1 

#     with open(track_pickle_path, 'rb') as file:
#         track_response_json = pickle.load(file)
#         track_result = keys2int(track_response_json)
#     save_video_name = generate_unique_filename(UPLOAD_FOLDER = sil_save_path, extension=None)
#     silhouette = seg_modified(video_path, track_result, sil_save_path, save_video_name, frame_rate_segment)
#     segment_folder = os.path.join(sil_save_path,save_video_name)
#     sil_pickle_path = os.path.join(pickle_path_seg,save_video_name)
#     with open(sil_pickle_path, 'wb') as file:
#         pickle.dump(silhouette, file)
#     segment_folder = fix_path(segment_folder)
#     sil_pickle_path = fix_path(sil_pickle_path)
#     res = {
#             "status": 1,
#             "error_code": None,
#             "error_message": None,
#             "result": 
#                 {
#            "segment_folder_path": segment_folder, 
#            'sil_pickle_path': sil_pickle_path
#                 }
#         }
#     print ('Done Segment')
#     return res




def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_seg:app", host=host_ip, port=int(seg_port_num), reload=True)


if __name__ == "__main__":
    main()