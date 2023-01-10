import numpy as np
import matplotlib.pyplot as plt
import json
import os
import cv2
import math

def draw_bbox(image, bbox):
    xmin, ytop, w, h = list(map(int, bbox))
    xmax = xmin + w
    ybot = ytop + h

    cv2.rectangle(image, (xmin, ytop), (xmax, ybot), (255,255,0), 2)

def get_bbox_center(bbox):
    x, y, w, h = bbox
    xc = x + 0.5*w
    yc = y + 0.5*h
    return xc, yc

def plot_image(image):
    plt.figure()
    plt.imshow(image)

def rotation(origin, point, angle):
    """ Rotate a point counterclockwise by a given angle around the origin. """
    ox, oy = origin
    px, py = point
    rx = px - ox
    ry = py - oy

    qx = ox + math.cos(angle) * rx - math.sin(angle) * ry
    qy = oy + math.sin(angle) * rx + math.cos(angle) * ry
    return int(qx), int(qy)


if __name__ == '__main__':
    path2anns = '../../data/video_orange_caps/annotations/anns_vials_down.json'
    path2imgs = '../../data/video_orange_caps/frames_cropped'
    with open(path2anns, 'r') as f:
        coco = json.load(f)
    
    anns = coco['annotations']
    image_ids = [ann['image_id'] for ann in anns]
    imgs = [img for img in coco['images'] if img['id'] in image_ids]

    imgid2ann = {}
    for ann in anns:
        image_id = ann['image_id']
        if image_id not in imgid2ann:
            imgid2ann[image_id] = []
        imgid2ann[image_id].append(ann)

    sel = 0
    img_d = imgs[sel]
    get_img = cv2.imread(os.path.join(path2imgs, img_d['file_name']))
    get_ann = imgid2ann[img_d['id']][0]

    x, y, w, h = get_ann['bbox']
    points = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]
    center = get_bbox_center(get_ann['bbox'])
    angle = get_ann['attributes']['rotation']
    rot_rect = (center, (h, w), angle%(2*np.pi))
    segm = cv2.boxPoints(rot_rect)
    segm = np.int0(segm)
    # segm = [rotation(pt, get_bbox_center(get_ann['bbox']), angl) for pt in rect]
    print(angle, segm)

    img_rect = cv2.drawContours(get_img, [segm], 0, (0,0,255), 2)
    cv2.imshow("Rotated Rectangle",get_img)
    cv2.waitKey()

    # draw_bbox(get_img, get_ann['bbox'])
    # plot_image(get_img[..., ::-1])
    # plt.show()
    