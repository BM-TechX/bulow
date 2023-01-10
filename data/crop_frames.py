import os
import cv2
import glob

# def click_event(event, x, y, flags, params):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         # Display coordinates on the shell
#         print(x, ' ', y)
        
#         # Display coordinates on the image window
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         cv2.putText(img, str(x) + ',' +
#                     str(y), (x,y), font,
#                     1, (255, 0, 0), 2)
#         cv2.imshow('image', img)
 
#     if event==cv2.EVENT_RBUTTONDOWN:
#         print(x, ' ', y)
        
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         b = img[y, x, 0]
#         g = img[y, x, 1]
#         r = img[y, x, 2]
#         cv2.putText(img, str(b) + ',' +
#                     str(g) + ',' + str(r),
#                     (x,y), font, 1,
#                     (255, 255, 0), 2)
#         cv2.imshow('image', img)

class Config:
    verbose = False

if __name__ == '__main__':
    path2frames = "/Users/pedromartinez/Library/CloudStorage/OneDrive-BusinessmannAS/novo_vibration_vials/data/frames_raw"
    path2dest = "/Users/pedromartinez/Library/CloudStorage/OneDrive-BusinessmannAS/novo_vibration_vials/data/frames_cropped"
    any_files = glob.glob(os.path.join(path2dest, '*'))
    for f in any_files:
        os.remove(f)

    file_names = os.listdir(path2frames)  # or glob.glob()
    for fn in file_names:
        if fn.endswith('.gif'):
            continue
        
        img = cv2.imread(os.path.join(path2frames, fn))
        if Config.verbose: 
            cv2.imshow('original', img)
            print(img.shape)

        x1, x2 = int(0.38*img.shape[1]), int(0.65*img.shape[1])  # left-right
        y1, y2 = int(0.25*img.shape[0]), int(0.80*img.shape[0])  # top-bottom
        img_cropped = img[y1:y2, x1:x2]
        img_cropped = cv2.resize(img_cropped, (530,550))          # ensure they're all the same size
        if Config.verbose:
            cv2.imshow("cropped", img_cropped)
            print(img_cropped.shape)
            
            # cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        cv2.imwrite(os.path.join(path2dest, '_cropped.'.join(fn.split('.'))), img_cropped)
