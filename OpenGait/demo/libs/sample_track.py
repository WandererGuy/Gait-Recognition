import os
import os.path as osp
import time
import sys
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from track import *
from fastapi import FastAPI, HTTPException, Form, Request
import uvicorn



app = FastAPI()

save_root = './demo/output/'
# gallery_video_path = "./demo/output/InputVideos/gallery.mp4"
# probe1_video_path  = "./demo/output/InputVideos/probe1.mp4"
# probe2_video_path  = "./demo/output/InputVideos/probe2.mp4"
# probe3_video_path  = "./demo/output/InputVideos/probe3.mp4"
# probe4_video_path  = "./demo/output/InputVideos/probe4.mp4"
current_script_directory = os.path.dirname(os.path.abspath(__file__))

import configparser
config = configparser.ConfigParser()
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
track_port_num = config['DEFAULT']['track_port_num'] 


@app.post("/write-result")
async def write_result(request: Request):
    data = await request.json()
    gallery_probe1_result = data["gallery_probe1_result"]
    probe1_video_path = data["probe1_video_path"]
    video_save_folder = data["video_save_folder"]
    # write the result back to the video
    writeresult(gallery_probe1_result, probe1_video_path, video_save_folder)
    return {'success': True}


@app.post("/tracking")
async def tracking(request: Request):
    
    data = await request.json()
    video_path = data["video_path"]
    output_dir = "./demo/output/OutputVideos/"
    os.makedirs(output_dir, exist_ok=True)
    current_time = time.localtime()
    # timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
    # video_save_folder = osp.join(output_dir, timestamp)
    video_save_folder = data["video_save_folder"]
    # tracking
    track_result = track(video_path, video_save_folder)
    
    output = {
        "video_path": video_path,
        "track_result": track_result,
    }
    print ('Done tracking ')
    return output
    
    
def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_track:app", host=host_ip, port=int(track_port_num), reload=True)

if __name__ == "__main__":
    main()