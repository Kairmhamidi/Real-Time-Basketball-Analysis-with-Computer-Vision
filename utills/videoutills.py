import cv2
import os

def VideoReader(FilePath):
    if not os.path.isfile(FilePath):
        raise ValueError("Video Does not Exist ")
    cap=cv2.VideoCapture(FilePath)

    frames=[]
    while True:
        ret,frame=cap.read()
        if not ret:
            break
        frame=cv2.flip(frame,1)
        frames.append(frame)
    return frames


def VideoWriter(frames,OutPutPath):
    if len(frames)==0:
        return
    if not os.path.exists(os.path.dirname(OutPutPath)):
        os.makedirs(os.path.dirname(OutPutPath))
    height,width,_=frames[0].shape
    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    out=cv2.VideoWriter(OutPutPath,fourcc,30.0,(width,height))
    for frame in frames:
        out.write(frame)
    out.release()