

import cv2

# Convert BGR to RGB for YOLO
def preprocess_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Extract usable detections (format: [x1, y1, x2, y2, class_name])
def postprocess_detections(results):
    boxes = results.xyxy[0].cpu().numpy()
    names = results.names
    return [
        [int(b[0]), int(b[1]), int(b[2]), int(b[3]), names[int(b[5])]]
        for b in boxes if b[4] > 0.4
    ]

# Dynamic scheduling based on lane count
def schedule_lights(counts):
    total = sum(counts)
    if total == 0:
        return [15] * len(counts)
    return [int((c / total) * 60) for c in counts]

# Overlay result info on frame
def draw_results(frame, counter, duration):
    text = f"Lane {counter.lane_id}: {counter.vehicle_count} vehicles | Green: {duration}s"
    cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    return frame
