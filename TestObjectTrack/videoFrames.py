import cv2
import os

def Readvideo(video_Path):
    cap=cv2.VideoCapture(video_Path)
    frames=[]
    while(cap.isOpened()):
        ret,frame=cap.read()
        if not ret:
            break
        frame=cv2.flip(frame,1)
        frames.append(frame)
    return frames


def videoWriter(videoPath,frames,fps):
    if not os.path.exists(os.path.dirname(videoPath)):
        height,width,channels=frames[0].shape
        os.makedirs(os.path.dirname(videoPath))
        fourcc=cv2.VideoWriter_fourcc(*'XVID')
        out=cv2.VideoWriter(videoPath,fourcc,fps,(width,height))
        for frame in frames:
            out.write(frame)
        out.release()
        