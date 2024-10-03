config_gpu = True # i set to cpu becuase cpu is faster than gpu lol , set to true if you want to use gpu
print ('decide to use gpu for paddle segmentation:', config_gpu)
from pathlib import Path

seg_yaml = "./demo/checkpoints/seg_model/human_pp_humansegv2_mobile_192x192_inference_model_with_softmax/deploy.yaml"
seg_yaml = Path(seg_yaml)
seg_cfgs = {  
    "model":{
        "seg_model" : seg_yaml,
    },
    "gait":{
        "dataset": "GREW",
    }
    }

import pickle
path = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/1e0d7c60-29a9-4994-be2f-c9297627272c"
with open (path, "rb") as f:
    tmp = pickle.load(f)
    print (tmp[0])
    
# import os 

# # Print the file size in kilobytes
# print(f"File size: {file_size_kb} KB")



