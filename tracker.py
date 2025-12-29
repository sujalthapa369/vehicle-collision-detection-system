from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

class CarTracker:
    def __init__(self):
        self.detector = YOLO("yolov8n.pt")
        self.tracker = DeepSort(max_age=30)

    def process(self, frame):
        results = self.detector(frame, classes=[2], conf=0.4)[0]
        detections = []

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append(([x1, y1, x2-x1, y2-y1], conf, "car"))

        tracks = self.tracker.update_tracks(detections, frame=frame)

        cars = []
        for t in tracks:
            if not t.is_confirmed():
                continue
            track_id = t.track_id
            x, y, w, h = map(int, t.to_ltrb())
            cx, cy = x + w//2, y + h//2

            cars.append({
                "id": track_id,
                "bbox": (x, y, x+w, y+h),
                "center": (cx, cy),
                "height": h
            })

        return cars
