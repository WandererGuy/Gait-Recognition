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

# import pickle
# path = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/embeddings_db/f2fa9ce7-aa5d-461e-8af9-0e40d986c037"
# with open (path, "rb") as f:
#     tmp = pickle.load(f)
#     print (tmp)
    
# import os 
# # Get the file size in bytes
# file_size_bytes = os.path.getsize("/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/segment/6c854a23-f8e1-4fbc-bde5-5f94ac838ffa")

# # Convert bytes to kilobytes
# file_size_kb = file_size_bytes / 1024

# # Print the file size in kilobytes
# print(f"File size: {file_size_kb} KB")



