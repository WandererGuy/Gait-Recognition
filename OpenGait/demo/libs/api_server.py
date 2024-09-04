import os
import sys
sys.path.append(os.path.abspath('.') + "/demo/libs/")
import requests
import json 
import ast
import pickle

url_tracking = 'http://10.0.68.103:8501/tracking'
url_seg = 'http://10.0.68.103:8502/segment'
url_rec = 'http://10.0.68.103:8503/extract-sil-function'
url_compare_multi = 'http://10.0.68.103:8503/compare-feat-multi'
url_compare_single = 'http://10.0.68.103:8503/compare-feat-single'

write_result = 'http://10.0.68.103:8501/write-result'

current_script_directory = os.path.dirname(os.path.abspath(__file__))





### only need to change input_video_name (every made folder will follow this name)
### put wanna write result video to same video save folder 
input_video_name = 'gallery.mp4'
video_save_folder_name = '1'



video_save_folder = os.path.dirname(current_script_directory)
video_save_folder = video_save_folder + '/output/OutputVideos/' + video_save_folder_name
# prob and gallery should be in same video_save_folder_name


current_script_directory = os.path.dirname(os.path.abspath(__file__))


# Get the absolute path of the directory containing the current script

pickle_path = os.path.join(current_script_directory,"pickle_variables")


folder_name = input_video_name.replace('.mp4','')
folder_path = os.path.join(pickle_path, folder_name)
print (folder_path)
os.makedirs(folder_path, exist_ok=True)



track_output_pickle = os.path.join(folder_path,"track_output.pickle")
rec_output_pickle = os.path.join(folder_path,"rec_output.pickle")
seg_output_pickle = os.path.join(folder_path,"seg_output.pickle")
final_output_pickle = os.path.join(folder_path,"final_output.pickle")
compare_output_pickle = os.path.join(folder_path,"compare_output.pickle")



def pickle_response(response, response_pickle_file):
    
    if response.status_code == 200:
        # Parse the JSON content from the response
        response = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")

    with open(response_pickle_file, 'wb') as file:
        # Serialize and write the variable to the file
        pickle.dump(response, file)

def keys2int(parent_key, sub_key_name):
    # Access the 'gallery_track_result' dictionary
    
    result = parent_key[sub_key_name]

    # Convert all keys to integers
    int_keys = {int(k): v for k, v in result.items()}

    # Replace the original dictionary with the modified one
    parent_key[sub_key_name] = int_keys
    return parent_key

                            # TRACK SERVER
gallery_video_path = os.path.dirname(current_script_directory) + '/output/InputVideos/' + input_video_name
path_dict = {'gallery_video_path': gallery_video_path, "video_save_folder": video_save_folder}
track_response = requests.post(url_tracking, json=path_dict)
pickle_response(track_response, track_output_pickle)


    
#                                 ## SEG 
                                
# with open(track_output_pickle, 'rb') as file:
#     # Deserialize and retrieve the variable from the file
#     track_response_json = pickle.load(file)
#     track_response_json = keys2int(track_response_json, 'gallery_track_result')
#     # track_response_json = keys2int(track_response_json, 'probe1_track_result')
    
# response = requests.post(url_seg, json=track_response_json)
# pickle_response(response, seg_output_pickle)



# #                                 #### REC SERVER
                                
# with open(seg_output_pickle, 'rb') as file:
#     # Deserialize and retrieve the variable from the file
#     seg_response_json = pickle.load(file)
#     seg_response_json["rec_output_pickle"] = rec_output_pickle

# response = requests.post(url_rec, json=seg_response_json)
# print (response)






# with open (track_output_pickle, 'rb') as file:
#     # Deserialize and retrieve the variable from the file
#     resopnse = pickle.load(file)
#     print (resopnse)
# with open (rec_output_pickle, 'rb') as file:
#     resopnse = pickle.load(file)
#     print (resopnse)
    
# with open (feat_pickle_file, 'rb') as file:
#     resopnse = pickle.load(file)
#     print (resopnse)




# #                             ## Compare muliple
                            
# gallery_name = "gallery" 
# probe1_name = "kien7"

# gallery_feat_path = os.path.join(pickle_path, gallery_name) + "/rec_output.pickle"
# probe1_feat_path  = os.path.join(pickle_path, probe1_name) + "/rec_output.pickle"

# input_compare_json = {"gallery_feat_path": gallery_feat_path,"probe1_feat_path": probe1_feat_path, "video_save_folder": video_save_folder}

# response = requests.post(url_compare_multi, json=input_compare_json)
# pickle_response(response, compare_output_pickle)




# ##                                # Compare single (single possibility bbox)
                                
# file_txt = open("/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/result_dist.txt", "w")
# file_txt.close()                             
                                
# gallery_name = "gallery" 
# probe1_name = "kien7"

# probe1_feat_path  = os.path.join(pickle_path, probe1_name) + "/rec_output.pickle"

# gallery_feat_path = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/GaitFeatures/gallery/006/undefined/undefined.pkl'
# id = '006'

# with open (probe1_feat_path, 'rb') as file:
#     # Deserialize and retrieve the variable from the file
#     probe1_feat = pickle.load(file)
#     print (probe1_feat)


# input_compare_json = {"gallery_feat_path": gallery_feat_path,
#                       "probe1_feat_path": probe1_feat_path, 
#                       "video_save_folder": video_save_folder, 
#                       "id": id, 
#                       "mode" : 'single'}

# response = requests.post(url_compare_single, json=input_compare_json)
# pickle_response(response, compare_output_pickle)


#                                 # Compare single (multi possibility bbox)
                                
# file_txt = open("/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/result_dist.txt", "w")
# file_txt.close()                             
                                
# gallery_name = "gallery" 
# probe1_name = "kien7"

# probe1_feat_path  = os.path.join(pickle_path, probe1_name) + "/rec_output.pickle"

# gallery_feat_path = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/GaitFeatures/gallery/006/undefined/undefined.pkl'
# id = '006'

# with open (probe1_feat_path, 'rb') as file:
#     # Deserialize and retrieve the variable from the file
#     probe1_feat = pickle.load(file)
#     print (probe1_feat)


# input_compare_json = {"gallery_feat_path": gallery_feat_path,
#                       "probe1_feat_path": probe1_feat_path, 
#                       "video_save_folder": video_save_folder, 
#                       "id": id, 
#                       "mode" : 'multi'}

# response = requests.post(url_compare_single, json=input_compare_json)
# pickle_response(response, compare_output_pickle)





#                             ### TRACK SERVER 
# with open (compare_output_pickle, 'rb') as file:
#     # Deserialize and retrieve the variable from the file
#     gallery_probe1_result = pickle.load(file)

#     gallery_probe1_result = gallery_probe1_result['output']["gallery_probe1_result"]     
#     probe1_video_path = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/OutputVideos/1/kien7.mp4"
#     video_save_folder = video_save_folder
           
                            
# loaded_data = None

# input = {
#     "gallery_probe1_result": gallery_probe1_result,
#     "probe1_video_path": probe1_video_path,
#     "video_save_folder": video_save_folder
#     }
# response = requests.post(write_result, json=input)
# pickle_response(response, final_output_pickle)
# final_resopnse = response.json()
# print (final_resopnse)







