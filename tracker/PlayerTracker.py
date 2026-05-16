
from ultralytics import YOLO
import supervision as sv
import sys
sys.path.append('./')
from utills.stubs_utils import ReadSub,Write_sub
class PlayerTracker:
    def __init__(self, modelPath):
        self.model = YOLO(modelPath)
        self.tracker = sv.ByteTrack()

    def detectFrames(self, frames):
        batchsize = 20
        detections = []

        for i in range(0, len(frames), batchsize):
            batchFrames = frames[i:i+batchsize]
            batchDetections = self.model.predict(batchFrames, conf=0.5)
            detections += batchDetections

        return detections

    def GetObjectTracker(self, frames,read_from_stub=False,stubPath=None):
        tracks=ReadSub(read_from_stub,stubPath)
        if tracks is not None:
            if len(tracks)==len(frames):
                return tracks
        detections = self.detectFrames(frames)
        tracks = []
        for frame_number, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v: k for k, v in cls_names.items()}

            detection_sv = sv.Detections.from_ultralytics(detection)
            detection_with_track = self.tracker.update_with_detections(detection_sv)

            tracks.append({})
            player_id = cls_names_inv.get("Player")
            if player_id is None:
                continue

            for i in range(len(detection_with_track)):
                bbox = detection_with_track.xyxy[i].tolist()
                cls_id = detection_with_track.class_id[i]
                track_id = detection_with_track.tracker_id[i]

                if track_id is None:
                    continue

                if cls_id == player_id:
                    tracks[frame_number][track_id] = {"box": bbox}
        if stubPath:
            Write_sub(stubPath,tracks)
        return tracks