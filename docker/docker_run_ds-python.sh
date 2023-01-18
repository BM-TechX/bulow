export DISPLAY=:1
xhost +
docker run -it --rm --net=host --runtime nvidia \
    -v /dev/bus/usb:/dev/bus/usb --privileged -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix/:/tmp/.X11-unix \
    -v /home/orin/bulow_project:/app \
    ds-python:runtime