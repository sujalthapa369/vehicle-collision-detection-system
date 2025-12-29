class DepthProxy:
    def __init__(self):
        self.depth_history = {}

    def update(self, cars):
        for c in cars:
            pseudo_depth = 1 / max(c["height"], 1)
            self.depth_history.setdefault(c["id"], []).append(pseudo_depth)

        return self.depth_history
