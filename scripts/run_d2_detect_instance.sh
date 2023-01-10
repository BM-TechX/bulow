python3 detectron2/demo/demo.py \
    --config-file outputs_d2/config.yaml \
    --video-input dataset/videos/video_blue_cap3.mp4 \
    --confidence-threshold 0.5 \
    --output video_predictions/detectron2/video_blue_cap3.mp4 \
    --opts MODEL.WEIGHTS outputs_d2/model_final.pth