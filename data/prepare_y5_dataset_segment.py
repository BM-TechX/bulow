import os
import glob
import json
import argparse
import numpy as np
import shutil
from PIL import Image

def traintest_split_images(image_paths, train_size=0.7, valid_size=0.15, test_size=0.15):
    from sklearn.model_selection import train_test_split
    X_train, X_ = train_test_split(image_paths, train_size=train_size, shuffle=True)
    if test_size == 0.0:
        return X_train, X_, []  # train and validation only

    if test_size == valid_size:
        split_ = 0.5
    else:
        split_ = valid_size/(1.0 - train_size)
    X_valid, X_test = train_test_split(X_, train_size=split_)
    return X_train, X_valid, X_test

def filter_images(images_list, annotations_list):
    img_ids = [ann["image_id"] for ann in annotations_list]
    images_list_ = [
        d_ for d_ in images_list if d_["id"] in img_ids
    ]
    # imgfname2idx = {d_["file_name"]: idx for idx, d_ in enumerate(images_list_)}
    return images_list_  #, imgfname2idx

def get_imgid2annids(anns_list):
    imgid2annsid = {}
    for ann in anns_list:
        ann_id = ann["id"]
        img_id = ann["image_id"]
        if img_id not in imgid2annsid:
            imgid2annsid[img_id] = [ann_id]
        else:
            imgid2annsid[img_id].append(ann_id)
    return imgid2annsid


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path2dataset', type=str, default='/home/orin/vibrator_project/dataset', help='path to data directory')
    parser.add_argument('--train_size', type=float, default=0.7, help='size of the train set')
    parser.add_argument('--valid_size', type=float, default=0.15, help='size of the validation set')
    parser.add_argument('--test_size', type=float, default=0.15, help='size of the test set')
    args = parser.parse_args()

    with open(os.path.join(args.path2dataset, "annotations/coco_annotations.json")) as f:
        coco_file = json.load(f)

    # some mappings
    anns_list = coco_file["annotations"]
    imgs_list = coco_file["images"]
    imgs_list = filter_images(imgs_list, anns_list)
    imgid2annids = get_imgid2annids(anns_list)
    annid2idx = {d_["id"]: idx for idx, d_ in enumerate(anns_list)}

    # split dataset: train, valid, test
    # image_fnames = [d_["id"] for d_ in imgs_list]
    train_set, valid_set, test_set = traintest_split_images(
        imgs_list, args.train_size, args.valid_size, args.test_size
    )

    class_id = 0  # only one class. NB: yolo class numbers must start from 0
    for set_name, set_ in zip(["train", "valid", "test"], [train_set, valid_set, test_set]):
        for img_dict in set_:
            # img_dict = imgs_list[imgfname2idx[fname]]
            img_fname = img_dict["file_name"]
            path2fname = os.path.join(
                args.path2dataset, 
                f"labels/{set_name}/{img_fname.split('.')[0]}.txt"
            )
            shutil.copyfile(
                os.path.join(args.path2dataset, f"images_all/{img_fname}"),
                os.path.join(args.path2dataset, f"images/{set_name}/{img_fname}")
            )
            W = img_dict["width"]
            H = img_dict["height"]
            img_id = img_dict["id"]
            ann_ids = imgid2annids[img_id]
            with open(path2fname, "w") as f:
                for i, ann_id in enumerate(ann_ids):
                    ann = anns_list[annid2idx[ann_id]]
                    segment = ann["segmentation"][0]

                    # yolo expects dims to be normalized
                    segment_y = [float(coord/W) if i%2 == 0 else float(coord/H) for i, coord in enumerate(segment)] + ["\n"]
                    yolo_array = [int(class_id)]
                    yolo_array += segment_y
                    for x in yolo_array[:-1]:
                        f.write("%s " % x)
                    f.write("%s" % yolo_array[-1])
