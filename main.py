from findframe import *
import cv2
import numpy as np
import sys


if __name__ == "__main__":
    # dataload
    videopath = sys.argv[1]
    cap = cv2.VideoCapture(str(videopath))
    curr_frame = None
    prev_frame = None
    frame_diffs = []
    frames = []
    success, frame = cap.read()
    i = 0
    FRAME = Frame(0, 0)
    while (success):
        luv = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        curr_frame = luv
        """
        
        calculate the difference between frames 
        
        """

        if curr_frame is not None and prev_frame is not None:
            diff = cv2.absdiff(curr_frame, prev_frame)
            diff_sum = np.sum(diff)
            diff_sum_mean = diff_sum / (diff.shape[0] * diff.shape[1])
            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            frames.append(frame)
        elif curr_frame is not None and prev_frame is None:
            diff_sum_mean = 0
            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            frames.append(frame)

        prev_frame = curr_frame
        i = i + 1
        success, frame = cap.read()
    cap.release()


    #detect the possible frame
    frame_return, start_id_spot_old, end_id_spot_old = FRAME.find_possible_frame(frames)

    #optimize the possible frame
    new_frame, start_id_spot, end_id_spot = FRAME.optimize_frame(frame_return, frames)

    #store the result
    start = np.array(start_id_spot)[np.newaxis, :]
    end = np.array(end_id_spot)[np.newaxis, :]
    spot = np.concatenate((start.T, end.T), axis=1)
    np.savetxt('./result.txt', spot, fmt='%d', delimiter='\t')
