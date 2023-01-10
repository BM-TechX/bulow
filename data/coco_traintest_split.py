import json
import os
from sklearn.model_selection import train_test_split
# TODO: implement cross validation (k-fold)

def filter_annotations(annotations, images):
    img_ids = [x['id'] for x in images]
    return [ann for ann in annotations if ann['image_id'] in img_ids]

def save_coco(file, info, licenses, images, annotations, categories):
    coco_dict = {
        'info'       : info,
        'licenses'   : licenses,
        'images'     : images,
        'annotations': annotations,
        'categories' : categories
    }
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump(coco_dict, coco, indent=2, sort_keys=True)
    
    return coco_dict

def coco_test_train_split(coco_anns, train_size, valid_size, verbose, p2train, p2valid, p2test):
    """
    Split COCO file of a whole dataset into train and test.
    Args:
        coco_anns    (dict): coco annotations
        train_size  (float): size of train dataset
        valid_size  (float): size of valid dataset
        verbose      (bool): show the sizes of the resulting datasets
    
    NB: the size of test dataset is inferred
    """
    info = coco_anns['info']
    lics = coco_anns['licenses']
    imgs = coco_anns['images']
    anns = coco_anns['annotations']
    cats = coco_anns['categories']

    # get the images with annotations only
    annid2imgid = {ann['id']: ann['image_id'] for ann in anns}
    imgs = [img for img in imgs if img['id'] in annid2imgid.values()]

    # TODO: include the case of having absolute sizes
    X_train, X_ = train_test_split(imgs, train_size=train_size, shuffle=True)
    X_valid, X_test = train_test_split(X_, train_size=valid_size)
    
    if verbose:
        print(f"train: {len(X_train)} ({len(X_train)/len(imgs):.2f})\n"  
              f"val: {len(X_valid)} ({len(X_valid)/len(imgs):.2f})\n"
              f"test: {len(X_test)} ({len(X_test)/len(imgs):.2f})")
    
    anns_train = filter_annotations(anns, X_train)
    anns_valid = filter_annotations(anns, X_valid)
    anns_test = filter_annotations(anns, X_test)

    train_coco_dict = save_coco(os.path.join(p2train, "coco_train.json"), info, lics, X_train, anns_train, cats)
    valid_coco_dict = save_coco(os.path.join(p2valid, "coco_valid.json"), info, lics, X_valid, anns_valid, cats)
    test_coco_dict = save_coco(os.path.join(p2test, "coco_test.json"), info, lics, X_test, anns_test, cats)

    return train_coco_dict, valid_coco_dict, test_coco_dict
    

        