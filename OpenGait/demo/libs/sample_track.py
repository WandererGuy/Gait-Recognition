import os
import os.path as osp
import time
import sys
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from track import *
from fastapi import FastAPI, HTTPException, Form, Request
import uvicorn
from utils_server.api_server import *



app = FastAPI()

current_script_directory = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_script_directory,"output","OutputVideos")
os.makedirs(output_dir, exist_ok=True)

import configparser
config = configparser.ConfigParser()
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
track_port_num = config['DEFAULT']['track_port_num'] 

ubuntu_prefix = '\\\\wsl.localhost\\Ubuntu-22.04\\'
# @app.post("/write-result")
# async def write_result(request: Request):
#     data = await request.json()
#     gallery_probe1_result = data["gallery_probe1_result"]
#     probe1_video_path = data["probe1_video_path"]
#     video_save_folder = data["video_save_folder"]
#     # write the result back to the video
#     writeresult(gallery_probe1_result, probe1_video_path, video_save_folder)
#     return {'success': True}
def check_file_exist(file_path): 
    if os.path.exists(file_path):
        return "File exists."
    else:
        return "File does not exist."


@app.post("/tracking")
async def tracking(video_path: str = Form(...), track_skip_frames: int = Form(...)):
    # current_time = time.localtime()
    # timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = output_dir, extension=None)

    video_save_folder = osp.join(output_dir, save_video_name)
    print ('------------------------------')
    print (check_file_exist(video_path))
    print (check_file_exist(video_save_folder))
    # tracking
    print (video_path)
    video_save_folder 
    print (video_save_folder)
    print (save_video_name)
    track_result = track(video_path, video_save_folder, save_video_name + '.mp4', track_skip_frames)
    track_video_folder = track_crop(video_path, track_result)
    print (track_video_folder)
    # with open(tmp, 'wb') as file:
    #     pickle.dump(track_result, file)
    # output_video_path = os.path.join(video_save_folder, save_video_name + '.mp4')
    # output_video_path = Path(output_video_path)
    output_path = os.path.join(current_script_directory, "OutputVideos", save_video_name)
    output = {
        "status": 1,
        "error_code": None,
        "error_message": None,
        "result":
            {
        "track_video_folder": fix_path(track_video_folder)
            }
    }
    print (f'Done tracking, saved in {fix_path(track_video_folder)}')
    return output
    
    
def main():
    print('INITIALIZING FASTAPI SERVER')
    # uvicorn.run("sample_track:app", host=host_ip, port=int(track_port_num), reload=True)
    uvicorn.run(app, host=host_ip, port=int(track_port_num), reload=False)

if __name__ == "__main__":
    main()