import numpy as np

def calculate_angle(a, b, c):
    """
    Calculates the 2D planar angle at vertex b (e.g. knee).
    a, b, c are [x, y] coordinates.
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360.0 - angle

    return angle

class RepetitionTracker:
    def __init__(self):
        self.counter = 0
        self.stage = "up"
        self.feedback = "Ready - Stand in View"

    def update(self, angle):
        if angle > 160:
            if self.stage == "down":
                self.counter += 1
                self.feedback = "Repetition Complete"
            self.stage = "up"
            if self.feedback != "Repetition Complete":
                self.feedback = "Descend to Target Depth"
        elif angle < 95:
            self.stage = "down"
            self.feedback = "Target Depth Achieved! Ascend"
        elif angle < 140 and self.stage == "up":
            self.feedback = "Flexing Joint - Continue Down"

        return self.counter, self.feedback, self.stage
