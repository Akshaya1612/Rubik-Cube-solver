import cv2
import json
import numpy as np

# Load HSV centers
with open("color_data.json", "r") as f:
    data = json.load(f)

COLOR_CENTERS = {
    name: np.array([vals["h"], vals["s"], vals["v"]], dtype=np.float32)
    for name, vals in data.items()
}

def classify_color(hsv_pixel):
    hsv_vec = np.array(hsv_pixel, dtype=np.float32)

    best_color = "unknown"
    best_dist = 999999

    for color, center in COLOR_CENTERS.items():
        dist = np.linalg.norm(hsv_vec - center)
        if dist < best_dist:
            best_dist = dist
            best_color = color

    # more forgiving threshold
    if best_dist > 120:
        return "unknown"

    return best_color

def ask_corrections(face_colors):
    print("\nDetected colors (1–9):")
    for i, c in enumerate(face_colors, start=1):
        print(f"{i}: {c}")

    ans = input("\nAre these correct? (y/n): ").strip().lower()

    if ans == "y":
        return face_colors

    print("\nEnter corrections:")
    print("Available colors: red, green, blue, yellow, white, orange")

    while True:
        pos = input("\nEnter position to change (1–9) or 'done': ")
        if pos.lower() == "done":
            break

        if not pos.isdigit() or not (1 <= int(pos) <= 9):
            print("Invalid position")
            continue

        new_color = input("Enter correct color: ").strip().lower()
        if new_color not in ["red","green","blue","yellow","white","orange"]:
            print("Invalid color")
            continue

        face_colors[int(pos)-1] = new_color
        print("Updated:", face_colors)

    print("\n✔ Final corrected face:", face_colors)
    return face_colors


# ===== CAMERA =====
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error")
    exit()

print("Press 'c' to capture. Press 'q' to quit.")

box_size = 40
gap = 50   # distance between grid squares

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    cx, cy = w//2, h//2
    start_x = cx - gap
    start_y = cy - gap

    # Draw 3×3 grid
    for r in range(3):
        for c in range(3):
            x = start_x + c*gap
            y = start_y + r*gap
            cv2.rectangle(frame, (x-15, y-15), (x+15, y+15), (0,255,0), 2)

    cv2.putText(frame, "Press C to capture, Q to quit", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Scan Cube Face", frame)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('c'):
        face_colors = []
        for r in range(3):
            for c in range(3):
                x = start_x + c*gap
                y = start_y + r*gap

                patch = frame[y-15:y+15, x-15:x+15]
                hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)

                H = int(np.mean(hsv[:,:,0]))
                S = int(np.mean(hsv[:,:,1]))
                V = int(np.mean(hsv[:,:,2]))

                color_name = classify_color((H,S,V))
                face_colors.append(color_name)

        # Ask for corrections
        final_face = ask_corrections(face_colors)
        print("\nSAVED FACE:", final_face)

    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
