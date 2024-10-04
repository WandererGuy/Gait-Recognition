tmp = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/TrackingResult"

gallery_video_folder_track_path_ls = []

probe_video_folder_track_path_l = []
import os 
import pickle 
p = "OpenGait/demo/libs/pickle_variables"
q = os.path.join(p, "people_session_info")
pickle_file_name = ""
pickle_file_path = os.path.join(q, pickle_file_name)
with open (pickle_file_path, 'rb') as file:
    if person.video_folder_track_path in 