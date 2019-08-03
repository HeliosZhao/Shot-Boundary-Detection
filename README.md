# Shot-Boundary-Detection

A shot is a series of frames that runs for an uninterrupted period of time. Shot Boundary Detection is detecting the first and last frame of a shot in a video.

## Requirement
* python3
* opencv-python
* opencv-contrib

## Algorithm
The basic algorithm I use is to calculate the difference between frames, because the larger the difference is, the more possible the frame is to be the boundary shot of a video. 
### My algorithm includes three steps: 
`1. Calculate all the differences between frames`

`2. Detect the possible frame`

  a. Create a window that includes 30 sequential frames, and select the frame that has the largest difference, which is called max_diff_frame in my code.
  
  b. Check whether the difference of the selected frame is more than 3 times the average difference of the other frames in the window. If the requirement mentioned above is met, regard the max_diff_frame as one of the possible frames. 
  
  c. Selected another 30 sequential frames after the max_diff_frame plus 8 frames, because I consider a spot should not be shorter than 8       frames. 
  
  d. Repeat b and c until all the frames are included into the window. 
  
`3. Optimize the possible frame` 

  a. Check whether the difference of the possible frame is no less than 10. 
  
  b. For every possible frame, check whether the difference is more than twice the average difference of the previous 10 frames and the subsequent 10 frames. If the requirements mentioned above are met, regard the possible frame as one of the boundary frames. 
  
## Result

Some examples of shots

The shot boundary detection result of a video `never say die` is the `result.txt`

