import argparse
from dataclasses import dataclass
import cv2
from kcf import Tracker
import glob
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="video or sequence you want to track", type=str)
    args = parser.parse_args()
    print(args)
    if 'avi'  in args.data or 'mp4' in args.data:
        args.video = args.data
        cap = cv2.VideoCapture(args.video)
        ok, frame = cap.read()
        tracker = Tracker()
        
        if not ok:
            print("error reading video")
            exit(-1)
        roi = cv2.selectROI("tracking", frame, False, False)
        #roi = (218, 302, 148, 108)
        tracker.init(frame, roi)
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break
            x, y, w, h = tracker.update(frame)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
            cv2.imshow('tracking', frame)
            c = cv2.waitKey(1) & 0xFF
            if c==27 or c==ord('q'):
                break
        cap.release()
        
    else:
        sequences = glob.glob(os.path.join(args.data, '*.jpg'))
        tracker = Tracker()
        
        if len(sequences) == 0:
            print("error reading video")
            exit(-1)

        for idx, img_file in enumerate(sequences):
            frame = cv2.imread(img_file)
            if idx == 0:
                roi = cv2.selectROI("tracking", frame, False, False)
                tracker.init(frame, roi)
            else:
                
                x, y, w, h = tracker.update(frame)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
                cv2.imshow('tracking', frame)
                c = cv2.waitKey(1) & 0xFF
                if c==27 or c==ord('q'):
                    break
         
    cv2.destroyAllWindows()