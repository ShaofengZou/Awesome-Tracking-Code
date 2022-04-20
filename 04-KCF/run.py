from re import S
import cv2
import argparse
import glob
import os
import kcftracker

selectingObject = False
initTracking = False
onTracking = False
ix, iy, cx, cy = -1, -1, -1, -1
w, h = 0, 0

inteval = 1
duration = 0.01

# mouse callback function


def draw_boundingbox(event, x, y, flags, param):
    global selectingObject, initTracking, onTracking, ix, iy, cx, cy, w, h

    if event == cv2.EVENT_LBUTTONDOWN:
        selectingObject = True
        onTracking = False
        ix, iy = x, y
        cx, cy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        cx, cy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        selectingObject = False
        if(abs(x - ix) > 10 and abs(y - iy) > 10):
            w, h = abs(x - ix), abs(y - iy)
            ix, iy = min(x, ix), min(y, iy)
            initTracking = True
        else:
            onTracking = False

    elif event == cv2.EVENT_RBUTTONDOWN:
        onTracking = False
        if(w > 0):
            ix, iy = x - w / 2, y - h / 2
            initTracking = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="video or sequence you want to track", type=str)
    args = parser.parse_args()
    print(args)

    tracker = kcftracker.KCFTracker(True, True, True)  # hog, fixed_window, multiscale
    # if you use hog feature, there will be a short pause after you draw a first boundingbox, that is due to the use of Numba.
    if 'avi' in args.data or 'mp4' in args.data:
        args.video = args.data
        cap = cv2.VideoCapture(args.video)

        ok, frame = cap.read()   
        if not ok:
            print("error reading video")
            exit(-1)
        roi = cv2.selectROI("tracking", frame, False, False)

        tracker.init(roi, frame)
        
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break
            bbox = tracker.update(frame)
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
            cv2.imshow('tracking', frame)
            c = cv2.waitKey(1) & 0xFF
            if c==27 or c==ord('q'):
                break
        cap.release()
    else:
        sequences = glob.glob(os.path.join(args.data, '*.jpg'))
        print('got sequences with %d frames' % len(sequences))
        if len(sequences) == 0:
            print("error reading video")
            exit(-1)

        for idx, img_file in enumerate(sequences):
            frame = cv2.imread(img_file)
            if idx == 0:
                roi = cv2.selectROI("tracking", frame, False, False)
                tracker.init(roi, frame)
            else:
                
                bbox = tracker.update(frame)
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
                cv2.imshow('tracking', frame)
                c = cv2.waitKey(1) & 0xFF
                if c==27 or c==ord('q'):
                    break
 
    cv2.destroyAllWindows()
