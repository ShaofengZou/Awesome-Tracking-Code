from csk import CSK
import cv2 # (Optional) OpenCV for drawing bounding boxes
import glob
import os

sequence_path = "datasets\\m1_rect_clip\\" # your sequence path
img_list = sorted(glob.glob(os.path.join(sequence_path, '*.jpg')))
save_path = "" # your save path

tracker = CSK() # CSK instance

for i, img_file in enumerate(img_list): # repeat for all frames
    frame = cv2.imread(img_file, 0)

    if i == 0: # 1st frame
        print(str(i)+"/"+str(len(img_list))) # progress
        init_gt = cv2.selectROI('demo', frame, False, False)
        [x1, y1, width, height] = init_gt
        tracker.init(frame,x1,y1,width,height) # initialize CSK tracker with GT bounding box
        img = cv2.rectangle(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR), (x1, y1), (x1+width, y1+height), (0,255,0), 2) # draw bounding box and save the frame

    else: # other frames
        print(str(i)+"/"+str(len(img_list))) # progress
        x1, y1 = tracker.update(frame) # update CSK tracker and output estimated position
        img = cv2.rectangle(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR), (x1, y1), (x1+width, y1+height), (0,255,0), 2)
    cv2.imshow('result', img)
    cv2.waitKey(100)
cv2.destroyAllWindows()