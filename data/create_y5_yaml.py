import os
import argparse
import yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path2dataset', type=str, default='/home/orin/vibrator_project/dataset', help='path to data directory')
    parser.add_argument('--yolovx', type=str, default='yolov5', help='yolo model to use')
    parser.add_argument('--label', type=str, default='platform')
    parser.add_argument('--yaml_fname', type=str, default='my_data_platform.yaml')
    args = parser.parse_args() 

    yaml_dict = {
        'path' : args.path2dataset,
        'train': "images/train",  # os.path.join(args.path2dataset, "images/train"),   # path to the train folder
        'val'  : "images/valid",  # os.path.join(args.path2dataset, "images/valid"),   # path to the valid folder
        'test' : "images/test",   # os.path.join(args.path2dataset, "images/test"),    # path to the test folder
        'nc'   : 1,
        'names': {0: args.label}
    }

    # path2yaml = args.path2dataset.replace('dataset', args.yolovx)
    # path2yaml = os.path.join(path2yaml, 'data/my_data.yaml')
    path2yaml = f"yolov5/data/{args.yaml_fname}"
    with open(path2yaml, 'w') as f:
        yaml.dump(yaml_dict, f)