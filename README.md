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