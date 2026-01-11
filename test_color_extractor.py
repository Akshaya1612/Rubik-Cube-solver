import cv2
import json
import numpy as np

# Load calibrated HSV centers
with open("color_data.json", "r") as f:
    data = json.load(f)

# Convert to numpy vectors
COLOR_CENTERS = {
    name: np.array([vals["h"], vals["s"], vals["v"]], dtype=np.float32)
    for name, vals in data.items()
}

def classify_color(hsv_pixel):
    """Return the closest color based on HSV distance."""
    hsv_vec = np.array(hsv_pixel, dtype=np.float32)
    best_color = "unknown"
    best_dist = 1e9

    for color, center in COLOR_CENTERS.items():
        dist = np.linalg.norm(hsv_vec - center)
        if dist < best_dist:
            best_dist = dist
            best_color = color

    # Optional: if too far from all known colors, mark as unknown
    if best_dist > 80:  # you can adjust this threshold
        return "unknown"

    return best_color

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: Camera not opening!")
    exit()

print("Move a cube sticker to the center. Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        print("❌ ERROR: Frame not captured.")
        break

    # draw center box
    h, w, _ = frame.shape
    size = 40
    cx, cy = w // 2, h // 2
    x1, y1 = cx - size, cy - size
    x2, y2 = cx + size, cy + size

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # get average HSV in center patch
    patch = frame[y1:y2, x1:x2]
    hsv_patch = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
    h_mean = int(np.mean(hsv_patch[:, :, 0]))
    s_mean = int(np.mean(hsv_patch[:, :, 1]))
    v_mean = int(np.mean(hsv_patch[:, :, 2]))

    detected = classify_color((h_mean, s_mean, v_mean))

    # show text
    cv2.putText(frame, f"HSV: ({h_mean},{s_mean},{v_mean})",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.putText(frame, f"Detected: {detected}",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Color Extractor Test", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
