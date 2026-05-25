import cv2
import sys
import numpy as np
sys.path.append('./')
from utills.bbox_utils import get_bbox_width,get_center_of_bbox

def drawTriangle(frame, bbox, color):
    y = int(bbox[1])
    x_center = int((bbox[0] + bbox[2]) / 2)
    trianglePoints = np.array([
        [x_center, y],
        [x_center - 10, y - 20],
        [x_center + 10, y - 20]
    ], dtype=np.int32)

    cv2.drawContours(frame, [trianglePoints], 0, color,cv2.FILLED)
    cv2.drawContours(frame,[trianglePoints],0,(0,0,0),2)
    return frame

def get_center_of_bbox(bbox):
    x1, y1, x2, y2 = bbox
    # Corrected: X is average of x1,x2; Y is average of y1,y2
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def drawElips(frame, bbox, color, trackID=None):
    x1, y1, x2, y2 = bbox
    x_center, y_center = get_center_of_bbox(bbox)
    
    # Position the ellipse near the feet (y2)
    # Adjusting cy slightly above the bottom line for a "perspective" look
    cy = int(y2) 
    
    # Draw the ellipse
    cv2.ellipse(
        frame,
        center=(x_center, cy),
        axes=(int((x2 - x1) * 0.5), int((x2 - x1) * 0.2)), # Width and height of ellipse
        angle=0,
        startAngle=-45,
        endAngle=235,
        color=color, 
        thickness=2
    )

    # Drawing the ID Tag (Rectangle + Text)
    if trackID is not None:
        rec_width = 40
        rec_height = 20
        x1_rec = x_center - rec_width // 2
        x2_rec = x_center + rec_width // 2  # Fixed: changed from - to +
        y1_rec = y2 - rec_height // 2
        y2_rec = y2 + rec_height // 2

        # Draw ID box
        cv2.rectangle(frame, (int(x1_rec), int(y1_rec)), (int(x2_rec), int(y2_rec)), color, cv2.FILLED)
        
        # Center the text in the box
        text_str = str(trackID)
        font_scale = 0.5
        thickness = 2
        text_size = cv2.getTextSize(text_str, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        text_x = x_center - text_size[0] // 2
        text_y = y1_rec + (rec_height + text_size[1]) // 2
        
        cv2.putText(frame, text_str, (int(text_x), int(text_y)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)

    return frame



