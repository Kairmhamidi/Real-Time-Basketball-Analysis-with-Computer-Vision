from utills.videoutills import VideoReader,VideoWriter
from tracker.PlayerTracker import PlayerTracker
from tracker.ballTracker import BallTracker
import os
import cv2
from drawers.PlayerTracks_drawer import PlayerTrackerDrawer
from drawers.BallTracks_drawer import BallTrackDrawer


video=os.path.join('input','video_1.mp4')
frames=VideoReader(video)

playerTracker=PlayerTracker('models/Basketball_player.pt')
playerTracks=playerTracker.GetObjectTracker(frames,read_from_stub=True,stubPath='stubes/playerTrackStubs.pkl')
playerTracksDrawer=PlayerTrackerDrawer()


balltraks=BallTracker('models/Basketball_player.pt')
ballTracks=balltraks.TrackFrames(frames,Read_from_stub=True,stubPath='stubes/ballTrackStubs.pkl')

# Remove Long ball detection
ballTracks=balltraks.remove_wrong_detection(ballTracks)
# InterPolation of Ball tracks:
ballTracks=balltraks.interpolate_ball_position(ballTracks)
outPutVideoFrames=playerTracksDrawer.draw(frames,playerTracks)
outPutVideoFrames=BallTrackDrawer().draw(outPutVideoFrames,ballTracks)

OutPutPath=os.path.join('Generator','video.avi')
VideoWriter(outPutVideoFrames,OutPutPath)

print(playerTracks)
