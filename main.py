from utills.videoutills import VideoReader,VideoWriter
from tracker.PlayerTracker import PlayerTracker
from tracker.ballTracker import BallTracker
import os
import cv2
from drawers.PlayerTracks_drawer import PlayerTrackerDrawer
from drawers.BallTracks_drawer import BallTrackDrawer
from team_asigner.team_asigner import teamAssiner
from ball_aquisition.ball_aquisition_detector import BallAquisitionDetector


video=os.path.join('input','video_1.mp4')
frames=VideoReader(video)

playerTracker=PlayerTracker('models/Basketball_player.pt')
playerTracks=playerTracker.GetObjectTracker(frames,
                                            read_from_stub=True,
                                            stubPath='stubes/playerTrackStubs.pkl')
playerTracksDrawer=PlayerTrackerDrawer()
balltraks=BallTracker('models/Basketball_player.pt')
ballTracks=balltraks.TrackFrames(frames,
                                 Read_from_stub=True,
                                 stubPath='stubes/ballTrackStubs.pkl')

# Remove Long ball detection
ballTracks=balltraks.remove_wrong_detection(ballTracks)
# InterPolation of Ball tracks:
ballTracks=balltraks.interpolate_ball_position(ballTracks)
# Asign Team player for each team based on the 
teamAsing=teamAssiner()
PlayerAssignment= teamAsing.get_player_team_across_fames(frames,
                                                         playerTracks,
                                                         True,
                                                         'stubes/player_assignment.pkl')

# Ball aquisition
ball_aquisition_detector= BallAquisitionDetector()
ball_aquisition=ball_aquisition_detector.detect_ball_position(playerTracks,ballTracks)
print(ball_aquisition)
outPutVideoFrames=playerTracksDrawer.draw(
    frames,
    playerTracks,
    PlayerAssignment,
    ball_aquisition
    )
outPutVideoFrames=BallTrackDrawer().draw(outPutVideoFrames,
                                         ballTracks
                                         )

OutPutPath=os.path.join('Generator','video.avi')
VideoWriter(outPutVideoFrames,OutPutPath)

