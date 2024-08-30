import os
import os.path as osp
import time
import sys
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from track import *
from fastapi import FastAPI, HTTPException, Form, Request
import uvicorn

host_ip = '10.0.68.103'
port_num = 8501

app = FastAPI()

save_root = './demo/output/'
# gallery_video_path = "./demo/output/InputVideos/gallery.mp4"
# probe1_video_path  = "./demo/output/InputVideos/probe1.mp4"
# probe2_video_path  = "./demo/output/InputVideos/probe2.mp4"
# probe3_video_path  = "./demo/output/InputVideos/probe3.mp4"
# probe4_video_path  = "./demo/output/InputVideos/probe4.mp4"

@app.post("/write-result")
async def write_result(request: Request):
    data = await request.json()
    gallery_probe1_result = data["gallery_probe1_result"]
    probe1_video_path = data["probe1_video_path"]

    # gallery_probe2_result = data[gallery_probe2_result]
    # gallery_probe3_result = data[gallery_probe3_result]
    # gallery_probe4_result = data[gallery_probe4_result]
    video_save_folder = data["video_save_folder"]
    # write the result back to the video
    writeresult(gallery_probe1_result, probe1_video_path, video_save_folder)
    # writeresult(gallery_probe2_result, probe2_video_path, video_save_folder)
    # writeresult(gallery_probe3_result, probe3_video_path, video_save_folder)
    # writeresult(gallery_probe4_result, probe4_video_path, video_save_folder)
    return {'success': True}


@app.post("/tracking")
async def tracking(request: Request):
    data = await request.json()
    gallery_video_path = data["gallery_video_path"]
    output_dir = "./demo/output/OutputVideos/"
    os.makedirs(output_dir, exist_ok=True)
    current_time = time.localtime()
    # timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
    # video_save_folder = osp.join(output_dir, timestamp)
    video_save_folder = data["video_save_folder"]
    # tracking
    gallery_track_result = track(gallery_video_path, video_save_folder)
    # probe1_track_result  = track(probe1_video_path, video_save_folder)
    # probe2_track_result  = track(probe2_video_path, video_save_folder)
    # probe3_track_result  = track(probe3_video_path, video_save_folder)
    # probe4_track_result  = track(probe4_video_path, video_save_folder)
    
    output = {
        "gallery_video_path": gallery_video_path,

        "gallery_track_result": gallery_track_result,
        # "probe1_track_result": probe1_track_result,
        # "probe2_track_result": probe2_track_result,
        # "probe3_track_result": probe3_track_result,
        # "probe4_track_result": probe4_track_result,
        "video_save_folder": video_save_folder, 
    }
    print ('Done tracking ')
    return output
    
    
def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("sample_track:app", host=host_ip, port=int(port_num), reload=True)

if __name__ == "__main__":
    main()