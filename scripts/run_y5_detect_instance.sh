git config --global --add safe.directory /jetson-inference/nissehue/yolov5

# TODO: crop frames

cd yolov5

python3 detect.py \
    --source ../dataset/videos/video_blue_cap3.mp4 \
    --weights runs/train/exp/weights/best.pt \
    --conf-thres 0.5