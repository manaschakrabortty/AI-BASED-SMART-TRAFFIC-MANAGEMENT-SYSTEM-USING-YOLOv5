
import cv2
import torch
import os
from my_utils import preprocess_frame, postprocess_detections, schedule_lights, draw_results
from lane_counter import LaneCounter
from display import display_result

# Load YOLOv5s model (from local or auto-download)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)

model.conf = 0.4  # confidence threshold

# Define video sources from data folder
video_paths = ['data/video1.mp4', 'data/video2.mp4', 'data/video3.mp4', 'data/video5.mp4']
captures = [cv2.VideoCapture(path) for path in video_paths]

# Initialize lane counters
lane_counters = [LaneCounter(i) for i in range(len(video_paths))]

while True:
    frames = []
    for cap in captures:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    if len(frames) < len(video_paths):
        break

    # Inference on each frame
    results = [model(preprocess_frame(f)) for f in frames]

    lane_counts = []
    for i, res in enumerate(results):
        boxes = postprocess_detections(res)
        count = lane_counters[i].count_vehicles(boxes)
        lane_counts.append(count)

    # Compute signal duration
    light_schedule = schedule_lights(lane_counts)

    # Display results per lane
    for i in range(len(frames)):
        frame_out = draw_results(frames[i], lane_counters[i], light_schedule[i])
        display_result(frame_out, i)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for cap in captures:
    cap.release()
cv2.destroyAllWindows()
