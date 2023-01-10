import json
import argparse

# GLOBAL
CATEGORIES = ["down"]

def coco_merge(path2coco_1, path2coco_2, path2ofile, save=False, indent=None):
    """
    Merge two COCO files from different batches into one for training. 
    Args:
        path2coco_1 (str): path to COCO file 1
        path2coco_2 (str): path to COCO file 2
        path2ofile  (str): path for output file
    """
    with open(path2coco_1, "r") as f1:
        d1 = json.load(f1)
    with open(path2coco_2, "r") as f2:
        d2 = json.load(f2)
    
    odict = {k: d1[k] for k in d1 if k not in ("images", "annotations")}  # output dict
    odict["images"] = []
    odict["annotations"] = []

    for i, data in enumerate([d1, d2]):
        catid_mapper_ = {}
        for new_cat in data["categories"]:
            new_id = None
            for ocat in odict["categories"]:
                if new_cat["name"] == ocat["name"]:
                    new_id = ocat["id"]
                    break

            if new_id is not None:
                catid_mapper_[new_cat["id"]] = new_id
            else:
                new_id = max(c["id"] for c in odict["categories"]) + 1
                catid_mapper_[new_cat["id"]] = new_id
                new_cat["id"] = new_id
                odict["categories"].append(new_cat)
        
        imgid_mapper_ = {}
        for img in data["images"]:
            n_imgs = len(odict["images"])
            imgid_mapper_[img["id"]] = n_imgs
            img["id"] = n_imgs
            odict["images"].append(img)
        
        for ann in data["annotations"]:
            n_anns = len(odict["annotations"])
            ann["id"] = n_anns
            ann["image_id"] = imgid_mapper_[ann["image_id"]]
            ann["category_id"] = catid_mapper_[ann["category_id"]]

            odict["annotations"].append(ann)
    odict["categories"] = [d_ for d_ in odict["categories"] if d_["name"] in CATEGORIES]
    if save:
        with open(path2ofile, "w") as f:
            json.dump(odict, f, indent=indent)

    return odict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path2coco_1', type=str)
    parser.add_argument('--path2coco_2', type=str)
    parser.add_argument('--path2ofile', type=str)
    parser.add_argument('--save', action="store_false")
    args = parser.parse_args() 

    coco_merge(args.path2coco_1, args.path2coco_2, args.path2ofile, save=args.save, indent=None)