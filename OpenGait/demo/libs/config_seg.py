def check_gpu_available():
    from paddleseg.utils import get_sys_env
    env_info = get_sys_env()
    print ('Paddle compiled with cuda:', env_info['Paddle compiled with cuda'] )
    print ('GPUs used:', env_info['GPUs used'])
    config_gpu = True if env_info['Paddle compiled with cuda'] \
        and env_info['GPUs used'] else False
    print ('config_gpu (use gpu) available:', config_gpu)
    return config_gpu

config_gpu = check_gpu_available() # set to true if you want to use gpu
print ("paddle compiled with cuda:", config_gpu) 
print ("decide to use gpu for paddle segmentation:", config_gpu)
from pathlib import Path

# seg_yaml = "./demo/checkpoints/seg_model/human_pp_humansegv2_mobile_192x192_inference_model_with_softmax/deploy.yaml"
seg_yaml = "./demo/checkpoints/seg_model/human_pp_humansegv1_server_512x512_inference_model_with_softmax/deploy.yaml"

seg_yaml = Path(seg_yaml)
seg_cfgs = {  
    "model":{
        "seg_model" : seg_yaml,
    },
    "gait":{
        "dataset": "GREW",
    }
    }



