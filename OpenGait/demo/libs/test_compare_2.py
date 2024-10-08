import os 
import pickle 

def multi_gallery_vs_single_probe(probe_feat_path, gallery_feat_path):
    import requests

    url = "http://10.0.68.103:2003/compare-embeddings-short"
    payload = {'probe_feat_path': probe_feat_path,
    'list_gallery_feat_path': gallery_feat_path}
    files=[
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    tmp = response.json()["result"]["distance"]
    return tmp
    
    # with open("demo/logs/log_compare.txt", "a") as f:
    #     for index, item in enumerate(tmp):
    #         f.write(f"Item {index}:\n")
    #         for key, value in item.items():
    #             f.write(f"{key}: {value}\n")
    #         f.write("\n")  # Add a blank line after each item for readability
            

if __name__ == "__main__":
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    tmp = os.path.dirname(current_script_directory)

    probe_person_folder_track_path_ls = [os.path.join(tmp,'output/TrackingResult/di vao 01h28p/001')]


    # probe_person_folder_track_path_ls = ["di vao 01h28p", "di ra 03h13p"]

    p = "demo/libs/pickle_variables"
    q = os.path.join(p, "people_session_info")
    pickle_file_name = "7c536af5-8b9d-4e61-a98c-0f73ff5bd382.pkl"
    pickle_file_path = os.path.join(q, pickle_file_name)


    list_gallery_feat_path = {}

    probe_dict = {}
    gallery_dict = {}
    with open ("demo/logs/log_compare.txt", "w") as f:
        pass

    with open (pickle_file_path, 'rb') as file:
        data = pickle.load(file)
        for person in data:
            print (person  )
            if person["person_folder_track_path"] in probe_person_folder_track_path_ls:
                probe_dict[person["person_folder_track_path"]] = person["embedding_path"]
            else:
                gallery_dict[person["person_folder_track_path"]] = person["embedding_path"]
                
    iterator = iter(probe_dict.values())
    probe_feat_path = next(iterator)

    list_gallery_feat_path = list(gallery_dict.values())
    distance_dict  = {}
    for person_folder_track_path, gallery_feat_path in gallery_dict.items():  
        distance = multi_gallery_vs_single_probe(probe_feat_path, gallery_feat_path)
        distance_dict[person_folder_track_path] = distance 
        # Sort dictionary by values from least to most
    sorted_dict = dict(sorted(distance_dict.items(), key=lambda item: item[1]))
    with open("demo/logs/log_compare.txt", "a") as f:
        for index, (key, value) in enumerate(sorted_dict.items()):
            f.write(f"Item {index}\n {key}\n {value}\n\n")

