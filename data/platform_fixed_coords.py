"""
Coordinates guide:

        x1,y1 ------
        |          |
        |          |
        |          |
        --------x2,y2

"""
import os
import glob
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
import cv2

def draw_rectangle(image, coords: tuple):
    """
    Draw rectangle on image
    """
    x1, y1, x2, y2 = coords
    if (x2 < x1) and (y2 < y1):
        w, h = x2, y2 
        x2 = x1 + w
        y2 = y1 + h
    if isinstance(image, str):
        # it's an image path
        image_pth = image
        image = cv2.imread(image)
    color = (255, 0, 0)
    thick = 2
    return cv2.rectangle(image, (x1, y1), (x2, y2), color, thick)

def main(args):
    fnames = glob.glob(os.path.join(args.path2images, "*.jpg"))
    load_i = cv2.imread(fnames[0])
    fnames = [os.path.basename(fname) for fname in fnames]

    H, W, c = load_i.shape
    images = [
        {"id": idx + 1, "width": W, "height": H, "file_name": fname}
        for idx, fname in enumerate(fnames)
    ]
    image_ids = [d_["id"] for d_ in images]

    x1, x2 = int(0.40*W), int(0.625*W) 
    y1, y2 = int(0.273*H), int(0.805*H)
    w = x2 - x1
    h = y2 - y1
    annotations = [
        {
            "id"          : idx + 1, 
            "image_id"    : id_, 
            "bbox"        : [x1, y1, w, h],
            "segmentation": [[]],
            "area"        : w*h,
            "category_id" : 1,
            "iscrowd"     : 0
        } for idx, id_ in enumerate(image_ids)]

    coco_dict = {
        "licenses"   : [{"name": "", "id": 0, "url": ""}],
        "info"       : {"contributor": "", "date_created": "", "description": "", "url": "", "version": "", "year": ""},
        "categories" : [{"id": 1, "name": "platform"}],
        "annotations": annotations,
        "images"     : images
    }

    with open(args.output_file, "w") as f:
        json.dump(coco_dict, f)

    if args.plot_img:
        fnames = glob.glob(os.path.join(args.path2images, "*.jpg"))
        img = draw_rectangle(fnames[0], (x1, y1, x2, y2))
        cv2.imwrite(f"deleteme.jpg", img)
    
    return coco_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path2images', type=str, 
                        default = '/home/orin/vibrator_project/dataset/images_allraw', 
                        help = 'path to images directory')
    parser.add_argument('--output_file', type=str, 
                        default = '/home/orin/vibrator_project/dataset/anotations/platform_fixed_coco_annotations.json', 
                        help = 'destination folder')
    parser.add_argument('--plot_img', action='store_true')
    args = parser.parse_args()

    main(args)
    
