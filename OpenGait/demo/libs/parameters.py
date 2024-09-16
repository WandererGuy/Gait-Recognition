config_gpu = True # i set to cpu becuase cpu is faster than gpu lol , set to true if you want to use gpu
print ('decide to use gpu for paddle segmentation:', config_gpu)

seg_cfgs = {  
    "model":{
        "seg_model" : "./demo/checkpoints/seg_model/human_pp_humansegv2_mobile_192x192_inference_model_with_softmax/deploy.yaml",
    },
    "gait":{
        "dataset": "GREW",
    }
    }

import pickle
with open ("E:/ManhT04/gait_2.0/Gait-Recognition/OpenGait/demo/libs/pickle_variables/segment/ed65828c-6030-484a-b3b3-7c92858b79a2.pickle", "rb") as f:
    tmp = pickle.load(f)
    print (tmp)