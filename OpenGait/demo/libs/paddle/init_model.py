import os 
current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_folder = os.path.dirname(current_script_directory)
import sys

sys.path.append(parent_folder)
from config_seg import config_gpu, seg_cfgs
from infer import Predictor_opengait
predictor = Predictor_opengait(seg_cfgs["model"]["seg_model"], config_gpu)
print ('Done initialize model into gpu')
