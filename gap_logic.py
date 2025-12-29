import numpy as np

class GapAnalyzer:
    def __init__(self, frame_height):
        self.gap_history = {}
        self.frame_height = frame_height

    def analyze(self, cars):
        # Sort cars by depth proxy (lower in image = closer)
        cars = sorted(cars, key=lambda c: c["center"][1], reverse=True)

        risk_pairs = []
        collision_pairs = []

        for i in range(len(cars) - 1):
            car_a = cars[i]
            car_b = cars[i + 1]

            gap = car_a["center"][1] - car_b["center"][1]
            key = (car_a["id"], car_b["id"])

            self.gap_history.setdefault(key, []).append(gap)

            history = self.gap_history[key]

            if len(history) < 6:
                continue

            # ===============================
            # 1️⃣ TEMPORAL SMOOTHING
            # ===============================
            smooth_gap = np.mean(history[-5:])

            # ===============================
            # 2️⃣ ADAPTIVE SAFE GAP
            # ===============================
            SAFE_GAP = 0.12 * self.frame_height  # adaptive

            # ===============================
            # 3️⃣ MOTION ENERGY SCORE
            # ===============================
            gap_velocity = np.gradient(history[-5:])
            motion_energy = abs(gap_velocity[-1])

            # ===============================
            # DECISION LOGIC
            # ===============================
            if smooth_gap < SAFE_GAP and motion_energy > 1.2:
                risk_pairs.append((car_a["id"], car_b["id"]))

            if smooth_gap < SAFE_GAP * 0.6 and motion_energy > 2.0:
                collision_pairs.append((car_a["id"], car_b["id"]))

        return risk_pairs, collision_pairs, self.gap_history
