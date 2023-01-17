import os
import sys
import argparse
import yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path2dataset', type=str, default='dataset/', help='path to data directory')
    parser.add_argument('--yolovx', type=str, default='yolov5', help='yolo model to use')
    parser.add_argument('--labels', type=str, default=None)
    parser.add_argument('--yaml_fname', type=str, default='my_data.yaml')
    args = parser.parse_args() 

    if args.labels is None:
        sys.exit("No labels passed!")

    labels = args.labels.split(',')

    yaml_dict = {
        'path' : args.path2dataset,
        'train': "images/train",  # os.path.join(args.path2dataset, "images/train"),   # path to the train folder
        'val'  : "images/valid",  # os.path.join(args.path2dataset, "images/valid"),   # path to the valid folder
        'test' : "images/test",   # os.path.join(args.path2dataset, "images/test"),    # path to the test folder
        'nc'   : len(args.labels),
        'names': {i: x for i, x in enumerate(args.labels)}
    }

    # path2yaml = args.path2dataset.replace('dataset', args.yolovx)
    # path2yaml = os.path.join(path2yaml, 'data/my_data.yaml')
    path2yaml = f"{args.yolovx}/data/{args.yaml_fname}"
    with open(path2yaml, 'w') as f:
        yaml.dump(yaml_dict, f)