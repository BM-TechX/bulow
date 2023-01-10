# has to be run inside container tensorrt

pip3 install -r TensorRT/requirements.txt
# pip3 install -e detectron2

python3 TensorRT/samples/python/detectron2/create_onnx.py \
    --exported_onnx model.onnx \
    --onnx model_converted.onnx \
    --det2_config outputs_d2/config.yaml \
    --det2_weights outputs_d2/model_final.pth \
    --sample_image dataset/images_all/frame_150_cropped.jpg
