import cv2
import json
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

colors = {}

print("Hold one face of the cube so that the CENTER sticker is inside the small square.")
print("Press SPACEBAR to capture the color.")
print("Press Q to quit after capturing all colors.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    size = 50
    cx, cy = w//2, h//2
    x1, y1 = cx-size, cy-size
    x2, y2 = cx+size, cy+size

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
    cv2.imshow("Color Calibration", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        patch = frame[y1:y2, x1:x2]
        hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
        h_mean = int(np.mean(hsv[:,:,0]))
        s_mean = int(np.mean(hsv[:,:,1]))
        v_mean = int(np.mean(hsv[:,:,2]))

        color_name = input("Enter color name (white, yellow, blue, green, red, orange): ")
        colors[color_name] = {"h": h_mean, "s": s_mean, "v": v_mean}
        print(f"Saved: {color_name} → {colors[color_name]}")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

with open("color_data.json", "w") as f:
    json.dump(colors, f, indent=4)

print("Calibration complete! Saved to color_data.json")
