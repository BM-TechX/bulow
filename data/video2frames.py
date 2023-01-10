"""
Script to break a video into frames. Things to take into account according to each video:
- locations: paths to the videos and destination folder for the frames
- start_time: sets what time start saving frames
- time_freq: every how many seconds save a frame
"""
import cv2
import os 
import re
import glob
import datetime
import matplotlib.pyplot as plt
import json

def varaince_of_laplacian(image):
    """
    This is a measure of the focus, i.e. how blurred it is.
    Args:
        image (np.ndarray): image of interest.
    Returns:
        Variance of the Laplacian filter on the image.
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()


def get_segmentation(image, color1, color2):
    """
    Segment objects based on their color.
    Args:
        image  (np.ndarray): image of interest.
        color1 (tuple)     : low threshold HSV color (low_H, low_S, low_V).
        color2 (tuple)     : high threshold HSV color (high_H, high_S, high_V).
    """
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # HSV color scale (cone)
    # cv2.imshow('HSV', imageHSV)
    # cv2.waitKey(10)
    mask = cv2.inRange(imageHSV, color1, color2)  # thresholding pixels
    return cv2.bitwise_and(image, image, mask=mask)


def plot_image(path2image):
    image = cv2.imread(path2image)
    plt.imshow(image)
    plt.show(image)


def video_duration(frames, fps):
    """ 
    Duration of the video.
    """
    video_dur = round(frames/fps)
    video_time = datetime.timedelta(seconds=video_dur)
    return video_time
    

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description = "Pipelines to fecth frames from a video.")
    path2data     = "/Users/pedromartinez/Library/CloudStorage/OneDrive-BusinessmannAS/novo_vibration_vials/data_allraw"
    path2frames   = "/Users/pedromartinez/Library/CloudStorage/OneDrive-BusinessmannAS/novo_vibration_vials/data/frames_raw"
    time_freq     = 1.0   # time step for saving frames
    verbose       = True
    number_frames = None
    blur_thr      = 300

    # Remove all (not-hidden) files from the folder
    any_frames = glob.glob(os.path.join(path2frames, '*'))
    # for f in any_frames:
    #     os.remove(f)

    path2json = "/Users/pedromartinez/Library/CloudStorage/OneDrive-BusinessmannAS/novo_vibration_vials/data_allraw/videos_info.json"
    with open(path2json, 'r') as f:
        videos_info = json.load(f)

    videos = glob.glob(os.path.join(path2data, "*.mp4"))
    for video in videos:
        video_nm = video.split('/')[-1].split('.')[0]
        print(f"\nGetting frames from {video_nm}")

        kv = video_nm[len('video_'):].split('cap')
        k_ = kv[0] + 'cap'  # color: blue, orange...
        v_ = kv[1]          # video number of that color
        if videos_info[k_][v_] == 0:
            # No tipped-over vials...
            continue

        cap = cv2.VideoCapture(video)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # total number of frames
        fps = cap.get(cv2.CAP_PROP_FPS)             # frequency (frames per second)
        # print(frames, fps)
        # if number_frames is not None:
        #     time_freq = 

        # Duration of the video
        video_time = video_duration(frames, fps)
        print(f"  Video duration: {video_time}")

        current_time = 0         # seconds, keeps track of current time
        if 'orange' in video_nm:
            start_time = 15000.  # in miliseconds
            cap.set(cv2.CAP_PROP_POS_MSEC, start_time)
            print(f"  Start time: {start_time/1000} sec")

        frame_num = 0  # current frame number
        time_laps = 0  # changes by 'time_freq' steps
        while True:
            success, frame = cap.read()
            if success:
                fm = varaince_of_laplacian(frame)
                if verbose:
                    ctime_ = round(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)  # seconds
                    cvtime_ = datetime.timedelta(seconds=ctime_)
                    if ctime_ - current_time >= 1:
                        # Print every second, and not every frame (saves memory)
                        print(f"  Timestamp: {cvtime_} - Frame num: {frame_num + 1} - Blur measure: {fm:.3f}")
                        current_time = ctime_
                    
                if fm > blur_thr:
                    frmS = cv2.resize(frame, (960, 540))
                    cv2.imshow('frm', frmS)
                    cv2.waitKey(10)
                    if frame_num/fps > time_laps:
                        cv2.imwrite(os.path.join(path2frames, f"{video_nm}_frame_{frame_num}.jpg"), frame)
                        time_laps += time_freq
            else:
                break
            frame_num += 1
        cap.release()
