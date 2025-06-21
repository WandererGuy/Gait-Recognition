# intro 
- this repository takes inspiration from (many thanks to their incredible work)
    - https://github.com/jdyjjj/All-in-One-Gait
    - https://github.com/ShiqiYu/OpenGait
- You can see their code and env, checkpoint prepare to understand thsi repository better
- I have improved upon their work: this repository handle 3 servers commincated with each other though FastAPI endpoints (microservice style)
- we have : tracking server, segment server, gait recogntion server

# Demo Results
- each person gets tracking bounding box and re-identification (this demo i took from  https://github.com/jdyjjj/All-in-One-Gait)
- but rest assured my repository can produce such result and even better since it is microservice rather than original monolith code base, and it can scale for multiple camera scenario
<div align="center">
       <img src="./OpenGait/demo/output/demo_video_result/gallery.gif"       width = "144" height = "256" alt="gallery" /> 
       <img src="./OpenGait/demo/output/demo_video_result/probe1-After.gif"  width = "455" height = "256" alt="probe1-After" />
       <img src="./OpenGait/demo/output/demo_video_result/probe2-After.gif"  width = "144" height = "256" alt="probe2-After" /> 
</div>


# prepare checkpoints 
see prepare_ckpts.md

# prepare environments
## intro
- this repository handle 3 servers commincated with each other though FastAPI endpoints (microservice style)
- we need to prepare env for each server , then turn each server on along with its env 
- we have : tracking server, segment server, gait recogntion server
- note that for tracking server , it requires linux system (since Bytetrack only works in linux) 

## instruction
- notice: each environment must be placed in 
    - ./OpenGait/all_env/env_track
    - ./OpenGait/all_env/env_seg
    - ./OpenGait/all_env/env_rec
- prepare env for tracking server, read instructions in prepare_env_track.md
- prepare env for segmentation server, read instruction in prepare_env_seg.md
- prepare env for recogntion server, read instruction in prepare_env_rec.md

# activate 3 servers 
in 3 different tewrminals , do each of this command
```
bash OpenGait\init_script\track.sh
```
```
bash OpenGait\init_script\seg.sh
```
```
bash OpenGait\init_script\rec.sh
```

# API usage 
visit each python script for more details
- demo/libs/sample_track.py
- demo/libs/sample_seg.py
- demo/libs/sample_rec.py