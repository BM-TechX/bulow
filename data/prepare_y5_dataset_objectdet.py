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
    imgid2idx = {d_["id"]: idx for idx, d_ in enumerate(images_list_)}
    return images_list_, imgid2idx


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path2dataset', type=str, default='dataset/', help='path to the yolov5 dataset')
    parser.add_argument('--path2images_all', type=str, default='images/')
    parser.add_argument('--path2annotations', type=str, default='annotations/')
    parser.add_argument('--json_fname', type=str, default='coco_annotations.json')
    parser.add_argument('--train_size', type=float, default=0.7, help='size of the train set')
    parser.add_argument('--valid_size', type=float, default=0.15, help='size of the validation set')
    parser.add_argument('--test_size', type=float, default=0.15, help='size of the test set')
    args = parser.parse_args()

    with open(os.path.join(args.path2annotations, args.json_fname)) as f:
        coco_file = json.load(f)

    # some mappings
    anns_list = coco_file["annotations"]
    imgs_list = coco_file["images"]
    imgs_list, imgid2idx = filter_images(imgs_list, anns_list)

    class_id = 0  # only one class. NB: yolo class numbers must start from 0
    yolo_labels = {}
    for ann in anns_list:
        ann_id = ann["id"]
        img_id = ann["image_id"]
        x, y, w, h = ann["bbox"]

        img_info = imgs_list[imgid2idx[img_id]]
        W = img_info["width"]
        H = img_info["height"]
        fname = img_info["file_name"]

        # yolo expects dims to be normalized
        xc, yc = (x + w/2)/W, (y + h/2)/H
        if fname not in yolo_labels:
            yolo_labels[fname] = [[class_id, xc, yc, w/W, h/H]]
        else:
            yolo_labels[fname].append([class_id, xc, yc, w/W, h/H])
    
    # split dataset: train, valid, test
    image_fnames = [d_["file_name"] for d_ in imgs_list]
    train_fnames, valid_fnames, test_fnames = traintest_split_images(
        image_fnames, args.train_size, args.valid_size, args.test_size
    )

    for set_name, set_fnames in zip(["train", "valid", "test"], [train_fnames, valid_fnames, test_fnames]):
        with open(os.path.join(args.path2dataset, set_name + '.txt'), 'w') as f:
            for fname in set_fnames:
                yolo_array = np.array(yolo_labels[fname])
                np.savetxt(
                    os.path.join(args.path2dataset, f"labels/{set_name}/{fname.split('.')[0]}.txt"),
                    yolo_array, 
                    fmt = ["%d", "%f", "%f", "%f", "%f"]  # format of the columns
                )

                shutil.copyfile(
                    os.path.join(args.path2images_all, fname),
                    os.path.join(args.path2dataset, f"images/{set_name}/{fname}")
                )

                # write {set_name}.txt files
                f.write(args.path2images_all + '\n')
