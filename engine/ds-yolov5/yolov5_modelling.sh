git clone https://github.com/marcoslucianops/DeepStream-Yolo.git

cp -R /opt/nvidia/deepstream/deepstream/sources/deepstream_python_apps/apps/common .
cp -R bulow/engine/ds-yolov5/app/* DeepStream-Yolo/
cp -R bulow/engine/ds-yolov5/configs/* DeepStream-Yolo/
cp -R bulow/engine/ds-yolov5/labels/* DeepStream-Yolo/
bash bulow/engine/ds-yolov5/models/get_engine_models.sh