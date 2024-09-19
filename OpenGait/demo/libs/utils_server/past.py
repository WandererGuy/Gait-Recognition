# def compare_multi_vs_multi():
#         gallery_name = "gallery" 
#         probe1_name = "kien7"

#         gallery_feat_path = os.path.join(pickle_path, gallery_name) + "/rec_output.pickle"
#         probe1_feat_path  = os.path.join(pickle_path, probe1_name) + "/rec_output.pickle"

#         input_compare_json = {"gallery_feat_path": gallery_feat_path,"probe1_feat_path": probe1_feat_path, "video_save_folder": video_save_folder}

#         response = requests.post(url_compare_multi, json=input_compare_json)
#         pickle_response(response, compare_output_pickle)


# def compare_single_gallery_get_single():
#         '''
#         given embedding probe to match, only 1 gallery get 1 match 
#         this is used more frequent 
#         '''
#         file_txt = open("/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/result_dist.txt", "w")
#         file_txt.close()                             
                                        
#         gallery_name = "gallery" 
#         probe1_name = "kien7"

#         probe1_feat_path  = os.path.join(pickle_path, probe1_name) + "/rec_output.pickle"

#         gallery_feat_path = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/GaitFeatures/gallery/006/undefined/undefined.pkl'
#         id = '006'

#         with open (probe1_feat_path, 'rb') as file:
#             # Deserialize and retrieve the variable from the file
#             probe1_feat = pickle.load(file)
#             print (probe1_feat)


#         input_compare_json = {"gallery_feat_path": gallery_feat_path,
#                             "probe1_feat_path": probe1_feat_path, 
#                             "video_save_folder": video_save_folder, 
#                             "id": id, 
#                             "mode" : 'single'}

#         response = requests.post(url_compare_single, json=input_compare_json)
#         pickle_response(response, compare_output_pickle)


# def compare_single_gallery_get_multi():
#         '''
#         given embeddings to match, multiple people can get 1 same embedding 
#         '''
#         file_txt = open("/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/result_dist.txt", "w")
#         file_txt.close()                             
                                        
#         gallery_name = "gallery" 
#         probe1_name = "kien7"

#         probe1_feat_path  = os.path.join(pickle_path, probe1_name) + "/rec_output.pickle"

#         gallery_feat_path = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/GaitFeatures/gallery/006/undefined/undefined.pkl'
#         id = '006'

#         with open (probe1_feat_path, 'rb') as file:
#             # Deserialize and retrieve the variable from the file
#             probe1_feat = pickle.load(file)
#             print (probe1_feat)


#         input_compare_json = {"gallery_feat_path": gallery_feat_path,
#                               "probe1_feat_path": probe1_feat_path, 
#                               "video_save_folder": video_save_folder, 
#                               "id": id, 
#                               "mode" : 'multi'}

#         response = requests.post(url_compare_single, json=input_compare_json)
#         pickle_response(response, compare_output_pickle)




# def compare_single_probe(gallery_vid_name, probe_vid_name):
#     '''
#     given lots of embedding in 1 vid , find the most similar embeds in those embed 
#     find distance , lets try multi first 
    
    
#     after then given an embedding store , find it 
#     each vid have embedding store 
    
#     not finding in embed store, it is find embed in the vid 
    
    
#     so given 2 vid embed extracted, find the most similar embed in those
#     one is gallery 
#     one is probe 
#     '''         
    
#     gallery_name = gallery_vid_name.replace(".mp4", "")
#     probe1_name = probe_vid_name.replace(".mp4", "")
#     distance_file_name = gallery_name + '_' + probe1_name

#     gallery_feat_path = os.path.join(pickle_path, gallery_name) + "/rec_output.pickle"
#     probe1_feat_path  = os.path.join(pickle_path, probe1_name) + "/rec_output.pickle"

#     input_compare_json = {"gallery_feat_path": gallery_feat_path,
#                         "probe1_feat_path": probe1_feat_path, 
#                         "video_save_folder": video_save_folder, 
#                         "distance_file_name": distance_file_name}

#     response = requests.post(url_compare_multi, json=input_compare_json)
#     pickle_response(response, compare_output_pickle)




#                             # TRACK SERVER
# gallery_video_path = os.path.dirname(current_script_directory) + '/output/InputVideos/' + input_video_name
# path_dict = {'gallery_video_path': gallery_video_path, "video_save_folder": video_save_folder}
# track_response = requests.post(url_tracking, json=path_dict)
# pickle_response(track_response, track_output_pickle)


    
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
