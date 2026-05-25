import sys
sys.path.append('/')
from drawers.utils import drawElips
from drawers.utils import  drawTriangle
class PlayerTrackerDrawer:
    def __init__(self,team_1_color=[255,245,238],team_2_color=[128,0,0]):
        self.default_player_id=1
        self.team_1_color=team_1_color
        self.team_2_color=team_2_color
    
    def draw(self,videoframes,tracks,playerAssignment,ball_aquisition):
        outPutvideoframe=[]
        for frame_number,frame in enumerate(videoframes):
            frame=frame.copy()
            playerDic=tracks[frame_number]
            player_has_the_ball=ball_aquisition[frame_number]
            # Draw players tracks
            Player_assignment_for_Frame=playerAssignment[frame_number]
            for trackID,player in playerDic.items():
                team_id=Player_assignment_for_Frame.get(trackID,self.default_player_id)
                if team_id==1:
                    color=self.team_1_color
                else:
                    color=self.team_2_color
                if trackID==player_has_the_ball:
                    frame=drawTriangle(frame,player['box'],(0,0,255))
                    
                frame=drawElips(frame,player['box'],color,trackID)
            outPutvideoframe.append(frame)
        return outPutvideoframe