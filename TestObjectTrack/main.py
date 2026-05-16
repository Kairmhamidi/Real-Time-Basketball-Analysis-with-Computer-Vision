# import sys
# import cv2
# from ultralytics import YOLO
# from videoFrames import Readvideo,videoWriter
# from PersonTracker import PersonTracker

# sys.path.append('/')

# model=YOLO('yolov8m.pt')
# video_path='input/video_1.mp4'

# # model.track(video_path,save=True)
# # save=True persist=True,  show=True, conf=0.5, save_txt=True,save_conf=True
# frames=Readvideo(video_path)


# TrackedFrames=PersonTracker('yolov8m.pt').TrackFrames(frames,ReadFromsub=True,subPath='checks/playerTrackStubs.pkl')
# ouPut_path='output/video_1.avi'


# videoWriter(ouPut_path,TrackedFrames,fps=30)

# print('Your Tracks values is  :',TrackedFrames[0].values())

import sys
import cv2
from ultralytics import YOLO
from videoFrames import Readvideo, videoWriter
from PersonTracker import PersonTracker

sys.path.append('/')

video_path = 'input/vid4.mp4'

# Read video frames
frames = Readvideo(video_path)
# Create tracker object
tracker = PersonTracker('yolov8m.pt')
# Get tracking data
TrackedFrames = tracker.TrackFrames(
    frames,
    ReadFromsub=True,
    subPath='checks/playerTrackStubs.pkl'
)

# Draw tracking on frames
outputVideoFrames = tracker.DrawTracks(
    frames,
    TrackedFrames
)

# Output path
ouPut_path = 'output/video_1.avi'

# Save video
videoWriter(
    ouPut_path,
    outputVideoFrames,
    fps=30
)

print('Your Tracks values is : ', TrackedFrames[0].values())