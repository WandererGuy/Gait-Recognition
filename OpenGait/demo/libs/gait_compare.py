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


def comparefeat(embs, probe_feat: dict, pid, threshold_value, gallery_id, all_compare):
    """Compares the distance between features

    Args:
        embs (Tensor): Embeddings of person with pid
        probe_feat (dict): Dictionary of features from probe
        pid (str): The id of person in gallery
        threshold_value (int): Threshold
    Returns:
        id (str): The id in probe
        dic_sort (dict): Recognition result sorting dictionary
    """
    gallery_name = pid.split("-")[0]
    min = threshold_value
    id = None
    dic={}
    # probe_feat = {'kien7': [{'006': {'undefined': tensor([[[-0.1423, -0.0651,  0.0327,  ...}
    # probe_feat[key] = []
    # probe_feat[key][0] = subject = {'006': {'undefined': tensor([[[-0.1423, -0.0651,  0.0327,  ...}
    for key in probe_feat:
        ### galery feat is a list of dict like  {'028': {'undefined': tensor([[[-0.1423, -0.0651,  0.0327,  ...,
        if key == gallery_name:
            continue
        
        for subject in probe_feat[key]:
            for type in subject:
                for view in subject[type]:
                    value = subject[type][view]
                    distance = computedistence(embs, value)
                    tmp = round(distance.item(), 5)
                    all_compare[f'probe:{type}-gallery:{gallery_id}'] = tmp

                    gid = key + "-" + str(type)
                    gid_distance = (gid, distance)
                    dic[gid] = distance
                    if distance.float() < min:
                        id = gid
                        min = distance.float()
    dic_sort= sorted(dic.items(), key=lambda d:d[1], reverse = False)
    if id is None:
        print("############## no id #####################")
    # dic = {'probe-006': tensor(18.9615, device='cuda:0')}
    # id = probe-006
    # dic_sort = [('probe-006', tensor(18.9615, device='cuda:0'))]
    return id, dic_sort, all_compare
