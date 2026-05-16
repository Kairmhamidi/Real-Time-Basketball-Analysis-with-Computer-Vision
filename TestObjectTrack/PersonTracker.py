# from ultralytics import YOLO
# import supervision as sv
# from Sub import Write_sub,ReadSub
# from drawUtils import drawEllipse
# class PersonTracker:
#     def __init__(self,modelPath):
#         self.model=YOLO(modelPath)
#         self.tracker=sv.ByteTrack()
#     def ReadFrames(self,frames):
#         detections=[]
#         batchSize=20
#         for i in range(0,len(frames),batchSize):
#             bathchedFrames=frames[i:i+batchSize]
#             batchDetection=self.model.predict(bathchedFrames)
#             detections+=batchDetection
#         return detections
#     def TrackFrames(self,frames,ReadFromsub=False,subPath=None):
#         if ReadFromsub:
#             tracks=ReadSub(ReadFromsub,subPath)
#             if tracks is not None and len(tracks)==len(frames):
#                 return tracks
#         detections=self.ReadFrames(frames)
#         Tracks=[]
#         for frameNumber,detection in enumerate(detections):
#             cls_names=detection.names
#             cls_sv={k:v for v,k in cls_names.items()}
#             svDetection=sv.Detections.from_ultralytics(detection)
#             detectionWithTrack=self.tracker.update_with_detections(svDetection)
#             Tracks.append({})
#             personID=cls_sv.get("person")
#             if personID is None:
#                 continue
#             for i in range(len(detectionWithTrack)):
#                 bbox=detectionWithTrack.xyxy[i].tolist()
#                 cls_id=detectionWithTrack.class_id[i]
#                 track_id=detectionWithTrack.tracker_id[i]
#                 if track_id is None:
#                     continue
#                 if cls_id==personID:
#                     Tracks[frameNumber][track_id]={"box":bbox}
#         Write_sub(subPath,Tracks)
#         return Tracks

    
from ultralytics import YOLO
import supervision as sv
from Sub import Write_sub, ReadSub
from drawUtils import drawEllipse

class PersonTracker:
    def __init__(self, modelPath):
        self.model = YOLO(modelPath)
        self.tracker = sv.ByteTrack()
    def ReadFrames(self, frames):
        detections = []
        batchSize = 20
        for i in range(0, len(frames), batchSize):
            bathchedFrames = frames[i:i + batchSize]
            batchDetection = self.model.predict(
                bathchedFrames,
                conf=0.5
            )
            detections += batchDetection
        return detections
    def TrackFrames(self, frames, ReadFromsub=False, subPath=None):
        if ReadFromsub:
            tracks = ReadSub(ReadFromsub, subPath)
            if tracks is not None and len(tracks) == len(frames):
                return tracks
        detections = self.ReadFrames(frames)
        Tracks = []
        for frameNumber, detection in enumerate(detections):
            cls_names = detection.names
            # {'person':0}
            cls_sv = {v: k for k, v in cls_names.items()}
            svDetection = sv.Detections.from_ultralytics(detection)
            detectionWithTrack = self.tracker.update_with_detections(
                svDetection
            )
            Tracks.append({})
            personID = cls_sv.get("person")
            if personID is None:
                continue
            for i in range(len(detectionWithTrack)):
                bbox = detectionWithTrack.xyxy[i].tolist()
                cls_id = detectionWithTrack.class_id[i]
                track_id = detectionWithTrack.tracker_id[i]
                if track_id is None:
                    continue
                if cls_id == personID:
                    Tracks[frameNumber][track_id] = {
                        "box": bbox
                    }

        Write_sub(subPath, Tracks)

        return Tracks

    def DrawTracks(self, videoFrames, tracks):

        outputVideoFrames = []

        for frameNumber, frame in enumerate(videoFrames):

            frame = frame.copy()

            playerDict = tracks[frameNumber]

            for track_id, player in playerDict.items():

                bbox = player["box"]

                drawEllipse(
                    frame,
                    bbox,
                    color=(0, 255, 0),
                    track_id=track_id
                )

            outputVideoFrames.append(frame)

        return outputVideoFrames