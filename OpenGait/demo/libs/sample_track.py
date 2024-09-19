import os
import os.path as osp
import time
import sys
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from track import *
from fastapi import FastAPI, HTTPException, Form, Request
import uvicorn
from utils_server.api_server import *

output_dir = "./demo/output/OutputVideos/"


app = FastAPI()

save_root = './demo/output/'
current_script_directory = os.path.dirname(os.path.abspath(__file__))

track_pickle_path = os.path.join(current_script_directory,"pickle_variables","track")
os.makedirs(track_pickle_path, exist_ok=True)

import configparser
config = configparser.ConfigParser()
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
track_port_num = config['DEFAULT']['track_port_num'] 


# @app.post("/write-result")
# async def write_result(request: Request):
#     data = await request.json()
#     gallery_probe1_result = data["gallery_probe1_result"]
#     probe1_video_path = data["probe1_video_path"]
#     video_save_folder = data["video_save_folder"]
#     # write the result back to the video
#     writeresult(gallery_probe1_result, probe1_video_path, video_save_folder)
#     return {'success': True}


@app.post("/tracking")
async def tracking(video_path: str = Form(...)):
    os.makedirs(output_dir, exist_ok=True)
    # current_time = time.localtime()
    # timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
    save_video_name = generate_unique_filename(UPLOAD_FOLDER = output_dir, extension=None)

    video_save_folder = osp.join(output_dir, save_video_name)
    # tracking
    track_result = track(video_path, video_save_folder, save_video_name + '.mp4')
    tmp = os.path.join(track_pickle_path, save_video_name)
    with open(tmp, 'wb') as file:
        pickle.dump(track_result, file)
    output_video_path = os.path.join(video_save_folder, save_video_name + '.mp4')
    output_video_path = Path(output_video_path)
    output = {
        "status": 1,
        "error_code": None,
        "error_message": None,
        "result":
            {
        "output_video_path": fix_path(output_video_path),
        "track_pickle_path": fix_path(tmp)
            }
    }
    print ('Done tracking')
    return output
    
    
def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_track:app", host=host_ip, port=int(track_port_num), reload=True)

if __name__ == "__main__":
    main()