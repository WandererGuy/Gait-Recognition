@app.post("/compare-embeddings-short")
async def compare_embeddings(
                            probe_feat_path: str = Form(...), 
                            list_gallery_feat_path: str  = Form(...)
                            ):
    compare_session = generate_unique_filename(UPLOAD_FOLDER = compare_session_folder, extension=None)
    probe_feat_path = Path(probe_feat_path)
    compare_session_save_path, ranking_ls = compare_multi_gallery_modified(
                         compare_session = compare_session,
                         probe_feat_path = probe_feat_path, 
                         list_gallery_feat_path = [list_gallery_feat_path], 
                         )
    print ('done compare')
            
    res = {
            "status": 1,
            "error_code": None,
            "error_message": None,
            "result": 
                {
                "distance": ranking_ls[0]["distance"],
                }
            }

    return res

def compare_multi_gallery_modified(compare_session, probe_feat_path, list_gallery_feat_path):
    input_compare_json = {"probe_feat_path": probe_feat_path,
                          "list_gallery_feat_path": list_gallery_feat_path, 
                          "session": compare_session}
    compare_session_save_path = compare_multi_gallery_video(input_compare_json)
    return compare_session_save_path

def compare_multi_gallery_video(data: dict):
    session = data["session"]
    list_gallery_feat_path = data["list_gallery_feat_path"]
    probe_feat_path = data["probe_feat_path"]
    with open(probe_feat_path, 'rb') as file:
        probe_feat = pickle.load(file)
    item_ls = []
    for index, gallery_feat_path in enumerate(tqdm(list_gallery_feat_path)):
            gallery_feat_path = Path(gallery_feat_path)
            if os.path.exists(gallery_feat_path):  
                with open(gallery_feat_path, 'rb') as file:
                    gallery_feat = pickle.load(file)
                    if gallery_feat == {}:
                        filename = gallery_feat_path.split("/")[-1]
                        logging.warning(f'{filename} gait feature empty because extracted feature extraction interuptted before or do not have person in it.')
                        continue
            else:
                filename = gallery_feat_path.split("/")[-1]
                logging.warning(f'{filename} did not extracted feature.')
                continue
            '''
            collect all feat from each id in each video and calculate distance
            so each id of each video = an item
            '''
            
            _, all_compare = compare(gallery_feat, probe_feat, mode = 'multi')
            for key, value in all_compare.items():
                item = {
                "probe_feat_path": fix_path(probe_feat_path),
                "gallery_feat_path": fix_path(gallery_feat_path),
                "probe_id" : key.split('-gallery')[0].split(':')[1],
                "gallery_id" : key.split('-gallery')[1].split(':')[1],
                "distance" : value
                }
                item_ls.append(item)
            
            compare_session_save_path = os.path.join(compare_session_folder,session + '.pkl')
            ranking_ls = display_all_distance(item_ls)
            with open (compare_session_save_path, 'wb') as file:
                pickle.dump(ranking_ls, file)
            
    return compare_session_save_path, ranking_ls



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

def computedistence(x, y):
    distance = torch.sqrt(torch.sum(torch.square(x - y)))
    return distanced
