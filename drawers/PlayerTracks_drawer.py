import sys
sys.path.append('/')
from drawers.utils import drawElips
class PlayerTrackerDrawer:
    def __init__(self):
        pass
    def draw(self,videoframes,tracks):
        outPutvideoframe=[]
        for frame_number,frame in enumerate(videoframes):
            frame=frame.copy()
            playerDic=tracks[frame_number]
            # Draw players tracks
            for trackID,player in playerDic.items():
                frame=drawElips(frame,player['box'],(0,0,255),trackID)
            outPutvideoframe.append(frame)
        return outPutvideoframe