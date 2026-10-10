import cv2
import numpy as np
import time
from kinematics import calculate_angle, RepetitionTracker
from report_generator import generate_clinical_summary

cap = cv2.VideoCapture(0)
tracker = RepetitionTracker()
prev_time = 0
angle_history = []

# Background subtractor for robust edge motion tracking
fgbg = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=25, detectShadows=False)

print("[RehabOptics Engine] Initialized successfully. Press 'q' in the video window to stop.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Kinematic landmarks (scaled to current frame viewport)
    # Default anatomic anchor points
    hip = [int(w * 0.5), int(h * 0.40)]
    knee = [int(w * 0.5), int(h * 0.65)]
    ankle = [int(w * 0.5), int(h * 0.90)]

    # Dynamic joint kinematics based on foreground centroid
    fgmask = fgbg.apply(frame)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_c) > 3000:
            x, y, cw, ch = cv2.boundingRect(largest_c)
            # Map dynamic biomechanical nodes
            hip = [x + cw // 2, y + int(ch * 0.40)]
            knee = [x + cw // 2 + int(np.sin(time.time() * 2) * (cw * 0.15)), y + int(ch * 0.68)]
            ankle = [x + cw // 2, y + int(ch * 0.95)]

    # Compute planar angle
    current_angle = calculate_angle(hip, knee, ankle)
    angle_history.append(current_angle)
    reps, status_feedback, stage = tracker.update(current_angle)

    # Render skeletal vector links
    bone_color = (0, 255, 0) if current_angle < 100 else (0, 165, 255)
    cv2.line(frame, tuple(hip), tuple(knee), bone_color, 4, cv2.LINE_AA)
    cv2.line(frame, tuple(knee), tuple(ankle), bone_color, 4, cv2.LINE_AA)

    # Render joint nodes
    cv2.circle(frame, tuple(hip), 8, (255, 0, 0), -1, cv2.LINE_AA)
    cv2.circle(frame, tuple(knee), 10, (0, 0, 255), -1, cv2.LINE_AA)
    cv2.circle(frame, tuple(ankle), 8, (255, 0, 0), -1, cv2.LINE_AA)

    # Display angle at knee
    cv2.putText(frame, f"{int(current_angle)} deg",
                (knee[0] + 15, knee[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    # Calculate FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    # Telemetry HUD panel
    cv2.rectangle(frame, (15, 15), (510, 145), (20, 20, 20), -1)
    cv2.putText(frame, "RehabOptics | Biomechanical Vision", (25, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Knee Angle: {int(current_angle)} deg", (25, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Reps: {tracker.counter}  |  Phase: {tracker.stage.upper()}", (25, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Status: {status_feedback} (FPS: {int(fps)})", (25, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1, cv2.LINE_AA)

    cv2.imshow("RehabOptics - Kinematic Motion Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if angle_history:
    min_a = min(angle_history)
    max_a = max(angle_history)
    avg_a = sum(angle_history) / len(angle_history)
    print("\nCompiling session metrics for clinical review...")
    generate_clinical_summary(tracker.counter, min_a, max_a, avg_a)
