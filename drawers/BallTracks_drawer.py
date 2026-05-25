import cv2
import numpy as np
import sys

sys.path.append('./')

from drawers.utils import drawTriangle

class BallTrackDrawer:
    def __init__(self):
        self.ball_pointer_color = (0, 255, 0)

    def draw(self, frames, tracks):
        outPutVideoFrame = []
        for frameNumber, frame in enumerate(frames):
            videoFrame = frame.copy()
            ballDic = tracks[frameNumber]
            for trackID, track in ballDic.items():
                bbox = track['box']
                if bbox is None:
                    continue
                videoFrame = drawTriangle(
                    videoFrame,
                    bbox,
                    self.ball_pointer_color
                )

            outPutVideoFrame.append(videoFrame)

        return outPutVideoFrame