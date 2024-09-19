import os
import os.path as osp
import pickle
import sys
# import shutil

root = os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__) )))
sys.path.append(root)
from opengait.utils import config_loader
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__)))) + "/modeling/")
from loguru import logger
import model.baselineDemo as baselineDemo
import gait_compare as gc

recognise_cfgs = {  
    "gaitmodel":{
        "model_type": "BaselineDemo",
        # "cfg_path": "./configs/baseline/baseline_GREW.yaml",
        "cfg_path": "./configs/gaitbase/gaitbase_da_gait3d.yaml",
    },
}


def loadModel(model_type, cfg_path):
    Model = getattr(baselineDemo, model_type)
    cfgs = config_loader(cfg_path)
    model = Model(cfgs, training=False)
    return model

def gait_sil(sils, embs_save_path):
    """Gets the features.

    Args:
        sils (list): List of Tuple (seqs, labs, typs, vies, seqL)
        embs_save_path (Path): Output path.
    Returns:
        feats (dict): Dictionary of features
    """
    gaitmodel = loadModel(**recognise_cfgs["gaitmodel"])
    gaitmodel.requires_grad_(False)
    gaitmodel.eval()
    feats = {}
    for inputs in sils:
        ipts = gaitmodel.inputs_pretreament(inputs)
        id = inputs[1][0]
        if id not in feats:
            feats[id] = []
        type = inputs[2][0] 
        view = inputs[3][0]
        embs_pkl_path = "{}/{}/{}/{}".format(embs_save_path, id, type, view)
        if not os.path.exists(embs_pkl_path):
            os.makedirs(embs_pkl_path)
        embs_pkl_name = "{}/{}.pkl".format(embs_pkl_path, inputs[3][0])
        retval, embs = gaitmodel.forward(ipts)
        pkl = open(embs_pkl_name, 'wb')
        pickle.dump(embs, pkl)
        feat = {}
        feat[type] = {}
        feat[type][view] = embs
        feats[id].append(feat)    
    return feats    


def gait_sil_modified(sils):
    """Gets the features.

    Args:
        sils (list): List of Tuple (seqs, labs, typs, vies, seqL)
        embs_save_path (Path): Output path.
    Returns:
        feats (dict): Dictionary of features
    """
    gaitmodel = loadModel(**recognise_cfgs["gaitmodel"])
    gaitmodel.requires_grad_(False)
    gaitmodel.eval()
    feats = {}
    for inputs in sils:
        ipts = gaitmodel.inputs_pretreament(inputs)
        id = inputs[1][0]
        if id not in feats:
            feats[id] = []
        type = inputs[2][0] 
        view = inputs[3][0]
        retval, embs = gaitmodel.forward(ipts)
        feat = {}
        feat[type] = {}
        feat[type][view] = embs
        feats[id].append(feat)    
    return feats    
def gaitfeat_compare(gallery_feat:dict, probe_feat:dict, mode):
    """Compares the feature between gallery and probe
    
    Args:
        gallery_feat (dict): Dictionary of gallery's features
        probe_feat (dict): Dictionary of probe's features
    Returns:
        pg_dicts (dict): The id of gallery corresponds to the id of probe
    """
    item = list(gallery_feat.keys())
    gallery = item[0]
    pg_dict = {}
    pg_dicts = {}
    dist_dict = {}
    all_compare = {}
    if mode == "multi":   
        for inputs in gallery_feat[gallery]:
            # input is like {'016': {'undefined': tensor([[[-0.1459,]]]
            number = list(inputs.keys())[0]
            galleryid = gallery + "-" + number
            # probe feat has many keys like '006'
            probeid, idsdict, all_compare = gc.comparefeat(inputs[number]['undefined'], probe_feat, galleryid, 100, number, all_compare)
            # [('probe-006', tensor(18.9615, device='cuda:0'))] 
            pg_dict[galleryid] = probeid
        # pg_dicts[galleryid] = idsdict
    else:
        for inputs in gallery_feat[gallery]:
            number = list(inputs.keys())[0]
            galleryid = gallery + "-" + number
            probeid, idsdict, all_compare = gc.comparefeat(inputs[number]['undefined'], probe_feat, galleryid, 100, number)
            # [('probe-006', tensor(18.9615, device='cuda:0'))] 
            dist_dict[galleryid] = idsdict
            pg_dict[galleryid] = None # all to None id 
        key_with_smallest_value = min(dist_dict, key=dist_dict.get)
        pg_dict[key_with_smallest_value] = probeid
        # pg_dicts[galleryid] = idsdict
    return pg_dict, all_compare

def extract_sil(sil, save_path):
    """Gets the features.

    Args:
        sils (list): List of Tuple (seqs, labs, typs, vies, seqL)
        save_path (Path): Output path.
    Returns:
        video_feats (dict): Dictionary of features from the video
    """
    logger.info("begin extracting")
    video_feat = gait_sil(sil, save_path)
    logger.info("extract Done")
    return video_feat

def extract_sil_modified(sil):
    """Gets the features.

    Args:
        sils (list): List of Tuple (seqs, labs, typs, vies, seqL)
        save_path (Path): Output path.
    Returns:
        video_feats (dict): Dictionary of features from the video
    """
    logger.info("begin extracting")
    video_feat = gait_sil_modified(sil)
    logger.info("extract Done")
    return video_feat

def compare(gallery_feat, probe_feat, mode = "multi"):
    """Recognizes  the features between probe and gallery

    Args:
        probe_feat (dict): Dictionary of probe's features
        gallery_feat (dict): Dictionary of gallery's features
    Returns:
        pgdict (dict): The id of probe corresponds to the id of gallery
    """
    logger.info("begin recognising")
    pgdict, all_compare = gaitfeat_compare(gallery_feat, probe_feat, mode = mode)
    logger.info("recognise Done")
    # print("================= probe - gallery aka pgdict ===================")
    # print(pgdict)
    return pgdict, all_compare