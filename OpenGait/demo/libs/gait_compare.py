import torch
import numpy as np

def getemb(data):
    return data["inference_feat"]

def computedistence(x, y):
    distance = torch.sqrt(torch.sum(torch.square(x - y)))
    return distance

def compareid(data, dict, pid, threshold_value):

    file_txt = open("/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/result_dist.txt", "a")
    probe_name = pid.split("-")[0]
    embs = getemb(data)
    min = threshold_value
    id = None
    dic={}
    for key in dict:
        if key == probe_name:
            continue
        for subject in dict[key]:
            for type in subject:
                for view in subject[type]:
                    value = subject[type][view]
                    distance = computedistence(embs["embeddings"],value)
                    gid = key + "-" + str(type)
                    gid_distance = (gid, distance)
                    dic[gid] = distance
                    if distance.float() < min:
                        id = gid
                        min = distance.float()
    dic_sort= sorted(dic.items(), key=lambda d:d[1], reverse = False)
    if id is None:
        print("############## no id #####################")
    return id, dic_sort


def comparefeat(embs, gallery_feat: dict, pid, threshold_value, probe_id, all_compare):
    """Compares the distance between features

    Args:
        embs (Tensor): Embeddings of person with pid
        gallery_feat (dict): Dictionary of features from gallery
        pid (str): The id of person in probe
        threshold_value (int): Threshold
    Returns:
        id (str): The id in gallery
        dic_sort (dict): Recognition result sorting dictionary
    """
    probe_name = pid.split("-")[0]
    min = threshold_value
    id = None
    dic={}
    # gallery_feat = {'kien7': [{'006': {'undefined': tensor([[[-0.1423, -0.0651,  0.0327,  ...}
    # gallery_feat[key] = []
    # gallery_feat[key][0] = subject = {'006': {'undefined': tensor([[[-0.1423, -0.0651,  0.0327,  ...}
    for key in gallery_feat:
        ### galery feat is a list of dict like  {'028': {'undefined': tensor([[[-0.1423, -0.0651,  0.0327,  ...,
        if key == probe_name:
            continue
        
        for subject in gallery_feat[key]:
            for type in subject:
                for view in subject[type]:
                    value = subject[type][view]
                    distance = computedistence(embs, value)
                    tmp = round(distance.item(), 5)
                    all_compare[f'gallery-{type}-probe-{probe_id}'] = tmp

                    gid = key + "-" + str(type)
                    gid_distance = (gid, distance)
                    dic[gid] = distance
                    if distance.float() < min:
                        id = gid
                        min = distance.float()
    dic_sort= sorted(dic.items(), key=lambda d:d[1], reverse = False)
    if id is None:
        print("############## no id #####################")
    # dic = {'gallery-006': tensor(18.9615, device='cuda:0')}
    # id = gallery-006
    # dic_sort = [('gallery-006', tensor(18.9615, device='cuda:0'))]
    return id, dic_sort, all_compare
