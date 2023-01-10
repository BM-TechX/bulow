#!/bin/sh
echo "root directory: ${PWD}"

exp_folder=${PWD}
path2dataset="${PWD}/dataset_segment"
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

# deal with the annotations
if [ -z "$(ls -A ${path2dataset}/annotations)" ]; then
    mkdir -p ${path2dataset}/annotations/batch_1
    mkdir -p ${path2dataset}/annotations/batch_2
    cd ${path2dataset}/annotations/batch_1
    wget https://vibratorvials.blob.core.windows.net/data/batch_1/b1_anns_vials_down.json
    cd ${path2dataset}/annotations/batch_2
    wget https://vibratorvials.blob.core.windows.net/data/batch_2/b2_anns_vials_down.json
    cd ${exp_folder}
    python3 vibration_vials/data/join_batches.py \
        --path2coco_1 ${path2dataset}/annotations/batch_2/b2_anns_vials_down.json \
        --path2coco_2 ${path2dataset}/annotations/batch_1/b1_anns_vials_down.json \
        --path2ofile ${path2dataset}/annotations/coco_annotations.json
fi

# download all the images
if [ -z "$(ls -A ${path2dataset}/images_all)" ]; then
    wget https://vibratorvials.blob.core.windows.net/data/batch_2/b2_frames_cropped.zip -O ${path2dataset}/images_all/b2_frames_cropped.zip
    wget https://vibratorvials.blob.core.windows.net/data/batch_1/b1_frames_cropped.zip -O ${path2dataset}/images_all/b1_frames_cropped.zip
    unzip ${path2dataset}/images_all/b2_frames_cropped.zip -d ${path2dataset}/images_all
    unzip ${path2dataset}/images_all/b1_frames_cropped.zip -d ${path2dataset}/images_all
    rm ${path2dataset}/images_all/b2_frames_cropped.zip
    rm ${path2dataset}/images_all/b1_frames_cropped.zip
    rm -R ${path2dataset}/images_all/__MACOSX
fi

cd ${exp_folder}
python3 vibration_vials/data/prepare_y5_dataset_segment.py \
    --path2dataset ${path2dataset} \
    --train_size 0.75 \
    --valid_size 0.15 \
    --test_size 0.15

python3 vibration_vials/data/create_y5_yaml.py \
    --path2dataset ${path2dataset} \
    --yolovx yolov5 \
    --label down \
    --yaml_fname my_data_vialsdown_segment.yaml