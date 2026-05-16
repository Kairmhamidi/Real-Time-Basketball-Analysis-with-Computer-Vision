import cv2
def drawEllipse(frame, bbox, color, track_id=None):
    x1, y1, x2, y2 = bbox
    # Convert to integers
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    # Center of player
    center_x = int((x1 + x2) / 2)
    center_y = int(y2)
    # Width of ellipse
    width = int((x2 - x1) / 2)
    # Draw ellipse
    cv2.ellipse(
        frame,
        center=(center_x, center_y),
        axes=(width, int(0.35 * width)),
        angle=0,
        startAngle=-45,
        endAngle=235,
        color=color,
        thickness=3,
        lineType=cv2.LINE_AA
    )
    # Draw ID box
    if track_id is not None:

        rectangle_width = 40
        rectangle_height = 20
        x1_rect = center_x - rectangle_width // 2
        x2_rect = center_x + rectangle_width // 2
        y1_rect = center_y + 15
        y2_rect = center_y + 15 + rectangle_height
        cv2.rectangle(
            frame,
            (x1_rect, y1_rect),
            (x2_rect, y2_rect),
            color,
            cv2.FILLED
        )
        cv2.putText(
            frame,
            f"{track_id}",
            (x1_rect + 10, y1_rect + 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            2
        )

    return frame