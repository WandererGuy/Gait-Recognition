import pickle

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
