#!/bin/sh
# has to be run from vibrator_vials repo
echo "root directory: ${PWD}"

exp_folder=${PWD}
path2dataset="${PWD}/dataset_objectdet"
path2images="${path2dataset}/images"
path2labels="${path2dataset}/labels"

mkdir -p ${path2dataset}
mkdir -p ${path2dataset}/images_all
mkdir -p ${path2dataset}/annotations
mkdir -p ${path2images}
mkdir -p ${path2images}/test
mkdir -p ${path2images}/valid
mkdir -p ${path2images}/train
mkdir -p ${path2labels}
mkdir -p ${path2labels}/test
mkdir -p ${path2labels}/valid
mkdir -p ${path2labels}/train

rm -rf ${path2images}/test/*
rm -rf ${path2images}/valid/*
rm -rf ${path2images}/train/*

rm -rf ${path2labels}/test/*
rm -rf ${path2labels}/valid/*
rm -rf ${path2labels}/train/*

rm -rf ${path2dataset}/*.txt
rm -rf ${path2dataset}/*.cache

# annotations
if [ -z "$(ls -A ${path2dataset}/annotations)" ]; then
    cd ${path2dataset}/annotations
    wget https://vibratorvials.blob.core.windows.net/data/platform_annotations.json -O coco_annotations.json
fi

# download all the images
if [ -z "$(ls -A ${path2dataset}/images_all)" ]; then
    cd ${path2dataset}/images_all
    wget https://vibratorvials.blob.core.windows.net/data/frames_raw/frames_raw.zip
    unzip frames_raw.zip
    rm frames_raw.zip
    rm -R __MACOSX
fi 

cd ${exp_folder}
python3 vibration_vials/data/prepare_y5_dataset_objectdet.py \
    --path2dataset ${path2dataset} \
    --train_size 0.75 \
    --valid_size 0.15 \

python3 vibration_vials/data/create_y5_yaml.py \
    --path2dataset ${path2dataset} \
    --yolovx yolov5 \
    --label down \
    --yaml_fname my_data_vialsdown_objectdet.yaml