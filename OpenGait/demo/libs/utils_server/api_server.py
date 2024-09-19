import pickle
import os
import uuid
def generate_unique_filename(UPLOAD_FOLDER, extension="txt"):
    if extension != None:
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return filename
    else:
        filename = f"{uuid.uuid4()}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return filename 

def pickle_response_modified(response, response_pickle_file):
    
    with open(response_pickle_file, 'wb') as file:
        # Serialize and write the variable to the file
        pickle.dump(response, file)


def pickle_response(response, response_pickle_file):
    
    if response.status_code == 200:
        # Parse the JSON content from the response
        response = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")

    with open(response_pickle_file, 'wb') as file:
        # Serialize and write the variable to the file
        pickle.dump(response, file)

# `def keys2int(dict, sub_key_name):
#     # Access the 'gallery_track_result' dictionary
#     tmp = dict[sub_key_name]

#     # Convert all keys to integers
#     int_keys = {int(k): v for k, v in tmp.items()}

#     # Replace the original dictionary with the modified one
#     dict[sub_key_name] = int_keys
#     return dict`

def keys2int(dict):
    # Access the 'gallery_track_result' dictionary

    # Convert all keys to integers
    new_dict = {int(k): v for k, v in dict.items()}

    # Replace the original dictionary with the modified one
    return new_dict

def get_target(text):
    # gallery-005-probe-011 : 17.2616
    target_gallery_id = text.split('-')[1]
    return target_gallery_id

def extract_target (file_path, target_gallery_id):
    target_distance_dict = {}
    target_gallery_id = str(target_gallery_id)
    with open (file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.split(' : ')
            if get_target(key) == target_gallery_id:
                target_distance_dict[key] = float(value)
    for i in target_distance_dict:
        print (i, target_distance_dict[i])
    return target_distance_dict  

import matplotlib.pyplot as plt
def plot_distance(target_distance_dict):       
        # Sorting the data by values in descending order
        sorted_gallery_probe_desc = dict(sorted(target_distance_dict.items(), key=lambda item: item[1], reverse=True))

        # Print the sorted dictionary
        print('=======================')
        for key, value in sorted_gallery_probe_desc.items():
            print(key, value)

        # Extract sorted keys and values for plotting
        sorted_galleries_desc = list(sorted_gallery_probe_desc.keys())
        sorted_values_desc = list(sorted_gallery_probe_desc.values())
        # Create a horizontal bar chart with larger figure size for better visualization
        plt.figure(figsize=(10, 8))
        max_value = max(sorted_values_desc)

        # Create a vertical bar chart
        plt.barh(sorted_galleries_desc, sorted_values_desc)
        tick_interval = 1

        # Set x-axis ticks with specific intervals (0.0, 2.5, 5.0, etc.)
        plt.xticks(ticks=[i for i in range(0, int(max_value + tick_interval), int(tick_interval))], 
                labels=[f'{i:.1f}' for i in range(0, int(max_value + tick_interval), int(tick_interval))])
        # Rotate the category labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Add labels and title
        # plt.xlabel('Categories')
        # plt.ylabel('Values')
        plt.title('distance calculate')
        
        # Adjust layout for better readability
        plt.tight_layout()
        save_path = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/ResultDistance/gallery_probe_plot.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print ('saved ', save_path)

def plot_target_distance(distance_file_path, target_gallery_id):
    target_distance_dict = extract_target(distance_file_path, target_gallery_id)  
    plot_distance(target_distance_dict) 

def check_name_in_list(my_list, element_to_check):
    # Check if the element is in the list
    if element_to_check in my_list:
        # Count occurrences
        count = my_list.count(element_to_check)
        return count
    else:
        return 0

def display_all_distance(data: list):
    dist_ls = []
    for item in data:
        distance = item['distance']
        dist_ls.append(distance) 
    sorted_ls = sorted(dist_ls)
    ranking_ls = []
    for i in range (len(sorted_ls)):
        index = dist_ls.index(sorted_ls[i])
        ranking_ls.append(data[index])
    return ranking_ls

# def display_all_distance(data: list):
#     dist_ls = []
#     dummy_value = 1000
#     for item in data:
#         distance = item['distance']
#         if item['gallery_feat_path'] == item["probe_feat_path"] and int(distance) < 0.1:
#             dist_ls.append(dummy_value) 
#             print ('gayyyyyyyy')
#         else:
#             print ('lessssss')
#             dist_ls.append(distance) 
#     sorted_ls = sorted(dist_ls)
#     ranking_ls = []
#     for i in range (len(sorted_ls)):
#         index = dist_ls.index(sorted_ls[i])
#         ranking_ls.append(data[index])
#     return ranking_ls

def change_pickle_path(pickle_path, saved_pickle_folder_name):
    new_pickle_path = os.path.join(pickle_path, saved_pickle_folder_name)
    return new_pickle_path

import numpy as np 
import json 
class NumpyEncoder(json.JSONEncoder): # turn dict with np array to be jsonizable
    # if need tensor send through http -> res = json.dumps(res, cls=NumpyEncoder)
    # here i have pickle cuda tensor so no need this 
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    
# def fix_path(path):
#     return path.replace('\\\\','/').replace('\\','/')