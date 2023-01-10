import json
import shutil
import numpy as np
from detectron2.structures import BoxMode, PolygonMasks
from skimage import measure

class DetectronCOCO(object):
    # TODO: append annotations to existing file
    def __init__(self, metadata, img_id=0):
        self.metadata = metadata
        self.img_id = img_id + 1
        self.cat_nms = metadata.thing_classes
        self.cat_id2name = {idx+1: nm for idx, nm in enumerate(self.cat_nms)}
        self.img_id2name = {}

        self.coco_images = []
        self.coco_annotations = []
        self.categories = [
            {"id": idx, "name": nm} 
            for idx, nm in self.cat_id2name.items()
        ]
        self.licenses = [{"name": "", "id": 0, "url": ""}]
        self.info = {"contributor": "", "date_created": "", "description": "", "url": "", "version": "", "year": ""}

        self.coco_dict = {
            "info"       : self.info, 
            "images"     : self.coco_images, 
            "categories" : self.categories,
            "licenses"   : self.licenses,
            "annotations": self.coco_annotations,
        }
    
    def _update_img_id(self, img_name):
        self.img_id2name[self.img_id] = img_name
        self.img_id += 1

    def mask_to_polygons(self, mask):
        # mask = np.ascontiguousarray(mask)
        # res = cv2.findContours(mask.astype("uint8"), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        # hierarchy = res[-1]
        # if hierarchy is None:  
        #     # empty mask
        #     return [], False
        # has_holes = (hierarchy.reshape(-1, 4)[:, 3] >= 0).sum() > 0
        # res = res[-2]
        # res = [x.flatten().astype("uint8").tolist() for x in res]
        # # res = [x + 0.5 for x in res if len(x) >= 6]
        cnts = measure.find_contours(mask, 0.5)
        segmentations = []
        for cnt in cnts:
            cnt = np.flip(cnt, axis=1)
            seg = cnt.ravel().tolist()
            segmentations.append(seg)
        return segmentations  # res, has_holes

    @staticmethod
    def _get_bbox_format(bbox):
        if not isinstance(bbox, np.ndarray):
            bbox = np.array(bbox)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        coco_bbox = [bbox[0], bbox[1], w, h]
        return coco_bbox

    def get_dict_from_prediction(self, prediction, fname):
        # TODO: include the option of object detection (bbox - no segmentation)
        # TODO: implement RLE encoding for segmentation
        fields = prediction['instances'].to('cpu')
        
        pred_masks = fields.pred_masks.numpy()
        _, ih, iw = pred_masks.shape
        coco_image = {
            'id'       : self.img_id,
            'width'    : iw,
            'height'   : ih,
            'file_name': fname
        }
        self.coco_images.append(coco_image)

        pred_classes = fields.pred_classes.numpy()
        for i, bbox in enumerate(fields.pred_boxes):
            segmentation = self.mask_to_polygons(pred_masks[i])
            polygons = PolygonMasks([segmentation])
            area = polygons.area()[0].item()
            d_ = {
                'id'          : len(self.coco_annotations) + 1,
                'image_id'    : self.img_id,
                'bbox'        : self._get_bbox_format(bbox.numpy().astype("float")),
                'area'        : area,
                'iscrowd'     : 0, 
                'category_id' : int(pred_classes[i]) + 1,
                'segmentation': [list(segmentation[0])]
            }
            self.coco_annotations.append(d_)

        self._update_img_id(fname)
    
    def save_coco_json(self, output_file):
        # tmp_file = output_file + ".tmp"
        with open(output_file, "w") as f:
            json.dump(self.coco_dict, f)
        # shutil.move(tmp_file, output_file)