import os
import cv2
#print(cv2.__version__)

'''
Summary of the keyframe sampling procedure:
D = duration of the video clip in seconds.
a) D < 1: extract the first and last frame.
b) D >= 1 and D < 11: three keyframes are extracted: first frame, 1 second and the last frame.
c) D > 11: keyframes are extracted at: first frame, time points = 1 s, 3 s, 5 s, 7 seconds etc. and the last frame.
'''

'''
Expected directory structure under video_root_path:  \<behaviour_class>\<individual_video_directory>\<video_file>
Note: all there may be muliple instances of directories at all levels in this path. The code will recurse through them all
'''

video_root_path = "./vids"

# set next True to extract every frame
extractEveryFrame = False

print "\n"

for behaviour_class in os.listdir(video_root_path):

    # print behaviour_class
    path = video_root_path + "/" + behaviour_class
    # print path
	
    for individual_video_directory in os.listdir(path):
        print behaviour_class +": "+ individual_video_directory
        videoPath = path + "/" + individual_video_directory
		
        for video_file in os.listdir(videoPath):
          framePath = videoPath + "/" + video_file
		  #if os.path.isdir(framePath):
          if video_file == "keyframes":
            # skip keyframes directory...it's not a video!
            continue
          print "This video is: " + video_file
          vidcap = cv2.VideoCapture(framePath)
          ''' next bit calculates approximate video length '''
          numberOfFrames = vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
          fps = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)
          if fps < 1: 
            fps = 25
          if numberOfFrames < 1: 
            numberOfFrames = 25
          videoLength = numberOfFrames / fps
          if videoLength < 1.0: 
            videoLength = 1.0
          print "numberOfFrames = " + str(numberOfFrames) + " fps = "  + str(fps)
          print "Clip duration = " + str(videoLength) + " seconds"
          ''' modes = EVERY_FRAME, SHORT_CLIP_FIRST_AND_LAST_FRAME, MEDIUM_CLIP_FIRST_AND_ONE_SECOND_AND_LAST, LONGER_CLIP_FIRST_AND_EVERY_TWO_SECONDS_AND_LAST '''
          if extractEveryFrame:
            mode = "EVERY_FRAME"
          elif videoLength < 1.0:
            mode = "SHORT_CLIP_FIRST_AND_LAST_FRAME"
          elif videoLength >= 1 and videoLength < 11:
            mode = "MEDIUM_CLIP_FIRST_AND_ONE_SECOND_AND_LAST"
          else: # videoLength > 11
              mode = "LONGER_CLIP_FIRST_AND_EVERY_TWO_SECONDS_AND_LAST"
          print "Mode = " + mode
          success,image = vidcap.read()
          count = 0
          success = True
          longerClip10SecondCounter = 1
          while success:
            success,image = vidcap.read()
            #if count == 0:
            if success:
             if mode == "SHORT_CLIP_FIRST_AND_LAST_FRAME":
               if count == 1 or count == numberOfFrames - 2: # numberOfFrames has to be adjusted -1 because count starts at 0, not sure why frames extracts numberOfFrames - 1. fps variable gets the frame at one second
                 print "Read frame #" + str(count) +" from: " + individual_video_directory + ":", success
                 cv2.imwrite(videoPath + "/keyframes/" + video_file+"_frame%d.jpg" % count, image)     # save frame as JPEG file
                 # print count
             elif mode == "MEDIUM_CLIP_FIRST_AND_ONE_SECOND_AND_LAST":
               if count == 1 or count == fps or count == numberOfFrames - 2:
                 print "Read frame #" + str(count) +" from: " + individual_video_directory + ":", success
                 cv2.imwrite(videoPath + "/keyframes/" + video_file+"_frame%d.jpg" % count, image)     # save frame as JPEG file
               # print count
             elif mode == "LONGER_CLIP_FIRST_AND_EVERY_TWO_SECONDS_AND_LAST":
               if count == longerClip10SecondCounter or count == numberOfFrames - 2:
                 longerClip10SecondCounter = longerClip10SecondCounter + (fps * 2)
                 print "Read frame #" + str(count) +" from: " + individual_video_directory + ":", success
                 cv2.imwrite(videoPath + "/keyframes/" + video_file+"_frame%d.jpg" % count, image)     # save frame as JPEG file
               # print count
             else: # mode must be "EVERY_FRAME"
               print "Read frame #" + str(count) +" from: " + individual_video_directory + ":", success
               cv2.imwrite(videoPath + "/keyframes/" + video_file+"_frame%d.jpg" % count, image)     # save frame as JPEG file
            count += 1
        print "\n"