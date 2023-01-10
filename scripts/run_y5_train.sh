# Must be run in the root folder ~/vibratorvials
#   bash scripts/run_train.sh

git config --global --add safe.directory /home/vibrator_project/yolov5

cd /home/vibrator_project/yolov5

python3 train.py \
    --img 512 \
    --batch 2  \
    --workers 4 \
    --epochs 30 \
    --data my_data_platform.yaml \
    --weights yolov5l.pt \
    --hyp data/hyps/hyp.scratch-low.yaml