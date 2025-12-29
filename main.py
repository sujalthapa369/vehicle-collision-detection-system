import cv2
from tracker import CarTracker
from gap_logic import GapAnalyzer
from depth_proxy import DepthProxy
from plot_utils import plot_depth, plot_gap

# ============================
# VIDEO PATH (MUST BE MP4)
# ============================
video_path = r"C:\Users\thapa\Downloads\videoplayback.mp4"

cap = cv2.VideoCapture(video_path)

# ============================
# SAFETY CHECKS (ORDER MATTERS)
# ============================
if not cap.isOpened():
    raise RuntimeError("❌ Cannot open video file. Use MP4 (H.264), not WEBM.")

ret, sample_frame = cap.read()
if not ret or sample_frame is None:
    raise RuntimeError("❌ Failed to read first frame. Video codec issue.")

frame_h, frame_w = sample_frame.shape[:2]

# Reset to first frame
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# ============================
# WINDOW CONFIG
# ============================
WINDOW_NAME = "Carrier Monitor"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

# ============================
# MODULES
# ============================
tracker = CarTracker()
gap_analyzer = GapAnalyzer(frame_height=frame_h)
depth_proxy = DepthProxy()

depth_history = {}
gap_history = {}

# ============================
# MAIN LOOP
# ============================
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cars = tracker.process(frame)
    risk_pairs, collision_pairs, gap_history = gap_analyzer.analyze(cars)
    depth_history = depth_proxy.update(cars)

    risk_ids = set(sum(risk_pairs, ()))
    collision_ids = set(sum(collision_pairs, ()))

    for c in cars:
        x1, y1, x2, y2 = c["bbox"]
        cid = c["id"]

        if cid in collision_ids:
            color = (0, 0, 255)
            label = "⚠ COLLISION"
        elif cid in risk_ids:
            color = (0, 255, 255)
            label = "RISK"
        else:
            color = (0, 255, 0)
            label = f"ID {cid}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
        cv2.putText(
            frame,
            label,
            (x1, y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    frame_resized = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
    cv2.imshow(WINDOW_NAME, frame_resized)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

plot_depth(depth_history)
plot_gap(gap_history)
