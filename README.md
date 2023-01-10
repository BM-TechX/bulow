# vibration_vials
Code for for Novo project: detecting tipped-over vials on a vibrating platform. 

If USB Basler camera is used, pylon SDKs are needed to get feed from it. To do so:

1. Download: https://www.baslerweb.com/en/downloads/software-downloads/software-pylon-7-2-1-linux-arm-64bit-debian/
2. ```tar -xf pylon_7.2.1.25747_aarch64_debs.tar.gz```
3. ```dpkg -i pylon_7.2.1.25747-deb0_arm64.deb```
4. ```sudo apt update && apt install swig```
5. ```git clone https://github.com/basler/pypylon.git```
6. ```cd pypylon```
7. ```pip3 install .```

Install the pylon gstreamer plugin from https://github.com/basler/gst-plugin-pylon.git

Include ```pylonsrc``` plugin in deepstream to get stream from USB Basler camera:

1. ```cd /opt/nvidia/deepstream/deepstream-6.1/sources/apps/apps-common/includes```
2. Edit file ```deepstream_sources.h```: include ```NV_DS_SOURCE_CAMERA_BASLER``` inside ```NvDsSourceType```
3. ```cd ../src```
4. Edit ```deepstream_source_bin.c```: add code to create pylonsrc element in ```create_camera_source_bin``` function. Example:
```bin -> src_elem = gst_element_factory_make(“pylonsrc”, “src_elem”)```.
