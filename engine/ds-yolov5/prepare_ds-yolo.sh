# run this in the project folder folder
cp -R /opt/nvidia/deepstream/deepstream/sources/deepstream_python_apps/apps/common .

# deepstream-yolo 
git clone https://github.com/marcoslucianops/DeepStream-Yolo.git
cp -R vibration_vials/engine/ds-yolov5/app/* DeepStream-Yolo/
cp -R vibration_vials/engine/ds-yolov5/configs/* DeepStream-Yolo/
cp -R vibration_vials/engine/ds-yolov5/labels/* DeepStream-Yolo/
cp vibration_vials/engine/ds-yolov5/auto_image_adjustx.pfs DeepStream-Yolo/
bash vibration_vials/engine/ds-yolov5/models/get_engine_models.sh

# signaling tower
cp vibration_vials/utils/signaling_fns.py DeepStream-Yolo/
