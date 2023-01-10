"""
I annotated the platform on a bunch of frames. Let's see if, by inspecting the mean
and spread of the middle point of the bboxes, we can assess if it moves much or not. 
SPOILER: it does not. 
"""
import os
import numpy as np
import json

# def load_annotations_COCO(path2anns: str):
#     """
#     Loads the annotations using COCO.
#     """
#     from pycocotools.coco import COCO

#     coco = COCO(path2anns)
#     return coco.anns

# def dyn_avg(val, avg, N):
#     return (N*avg + val)/(N+1)

def get_center_bbox(x, y, w, h):
    if not isinstance(x, np.ndarray):
        x, y = np.array(x), np.array(y)
        w, h = np.array(w), np.array(h)
    xc = x + w/2
    yc = y + h/2
    return xc, yc

if __name__ == '__main__':
    path_ = os.getcwd()
    path2json = os.path.join(path_, '../../data/video_orange_caps/annotations/anns_platform.json')
    # anns = load_annotations(path2json)
    with open(path2json, 'r') as f:
        data_ann = json.load(f)
    
    # Annotations
    anns = data_ann['annotations']
    anns_total = len(anns)
    print(f"\nNumber of images: {anns_total}")

    xs, ys = [], []
    ws, hs = [], []
    for ann in anns:
        bbox_ = ann['bbox']
        xs.append(bbox_[0])
        ys.append(bbox_[1])
        ws.append(bbox_[2])
        hs.append(bbox_[3])

    xcs, ycs = get_center_bbox(xs, ys, ws, hs)

    print("\nBounding boxes:")
    print(f"  Avg xleft: {np.mean(xs):.2f} +/- {np.std(xs):.2f}")
    print(f"  Avg ytop: {np.mean(ys):.2f} +/- {np.std(ys):.2f}")
    print(f"  Avg W: {np.mean(ws):.2f} +/- {np.std(ws):.2f}")
    print(f"  Avg H: {np.mean(hs):.2f} +/- {np.std(hs):.2f}")
    print(f"  Avg xcenter: {np.mean(xcs):.2f} +/- {np.std(xcs)}")
    print(f"  Avg ycenter: {np.mean(ycs):.2f} +/- {np.std(ycs)}")

    # Images
    img_ws, img_hs = [], []
    for img_dict in data_ann['images']:
        img_ws.append(img_dict['width'])
        img_hs.append(img_dict['height'])
    print("\nImages:")
    print(f"  Widths: {np.unique(img_ws)}")
    print(f"  Heights: {np.unique(img_hs)}")

    # Pecentages
    print(np.mean(xs)/np.unique(img_ws)[0], (np.mean(xs)+np.mean(ws))/np.unique(img_ws)[0])
    print(np.mean(ys)/np.unique(img_hs)[0], (np.mean(ys)+np.mean(hs))/np.unique(img_hs)[0])