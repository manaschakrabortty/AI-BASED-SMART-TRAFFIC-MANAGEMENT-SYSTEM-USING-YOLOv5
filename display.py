
import cv2

def display_result(frame, lane_id):
    window = f"Lane {lane_id + 1}"
    cv2.imshow(window, frame)
