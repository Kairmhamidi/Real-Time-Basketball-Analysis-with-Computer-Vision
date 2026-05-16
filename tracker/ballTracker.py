from ultralytics import YOLO
import sys
import supervision as sv
import numpy as np

sys.path.append('./')
from utills.stubs_utils import ReadSub,Write_sub
class BallTracker:
    def __init__(self,modelPath):
        self.model=YOLO(modelPath)
        self.tracker=sv.ByteTrack()
    def GetFrames(self,frames):
        detections=[]
        batch=20
        for i in range(0,len(frames),batch):
            batchFrames=frames[i:i+batch]
            batchDetection=self.model.predict(batchFrames)
            detections+=batchDetection
        return detections
    def TrackFrames(self,frame,Read_from_stub=False,stubPath=None):
        if Read_from_stub:
            tracks=ReadSub(Read_from_stub,stubPath)
            if tracks is not None and len(tracks)==len(frame):return tracks
        tracks=[]
        detections=self.GetFrames(frame)
        for frame_number,detection in enumerate(detections):
            cls_names=detection.names
            cls_name_env={k:v for v,k in cls_names.items()}
            svDetection=sv.Detections.from_ultralytics(detection)
            tracks.append({})
            max_conf=0
            choosen_box=None
            for frameDetection in svDetection:
                bbox=frameDetection[0].tolist()
                cls_id=frameDetection[3]
                conf=frameDetection[2]
                if cls_id == cls_name_env.get('Ball'):
                    if conf>max_conf:
                        choosen_box=bbox
                        max_conf=conf
                if choosen_box is not None:
                    tracks[frame_number][1]={ 'box':choosen_box}
        if stubPath:
            Write_sub(stubPath,tracks)
        return tracks
    def remove_wrong_detection(self,ball_position):
        max_allowed_distance=25
        last_good_frame_index=-1
        for i in range(len(ball_position)):
            current_box=ball_position[i].get(1,{}).get('box',[])
            if len(current_box)==0:
                continue
            if last_good_frame_index==-1:
                last_good_frame_index=i
                continue
            last_good_box=ball_position[last_good_frame_index].get(1,{}).get('box',[])
            frame_gap=i-last_good_frame_index
            adjusted_max_distance=max_allowed_distance+frame_gap
            # Calculate the distanec between the last good bbx and current position
            if np.linalg.norm(np.array(last_good_box[:2])-np.array(current_box[:2]))>adjusted_max_distance:
                ball_position[i]={}
                




