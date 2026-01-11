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

    if best_dist > 120:
        return "unknown"

    return best_color


def correct_face(colors):
    print("\nDetected colors:")
    print(colors)

    ans = input("\nAre these correct? (y/n): ").lower()
    if ans == "y":
        return colors

    print("\nEnter corrections (type 'done' to finish)")
    print("Colors: red, green, blue, yellow, white, orange\n")

    while True:
        pos = input("Enter position to change (1–9) or 'done': ")
        if pos == "done":
            break

        if not pos.isdigit() or not (1 <= int(pos) <= 9):
            print("Invalid position.")
            continue

        new_color = input("Enter correct color: ").lower()
        if new_color not in ["red","green","blue","yellow","white","orange"]:
            print("Invalid color.")
            continue

        colors[int(pos)-1] = new_color
        print("Updated:", colors)

    return colors


def scan_one_face(window_name, cap):
    print(f"\n➡ Place the {window_name} face inside the grid and press C.")

    box_size = 40
    gap = 50

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        h, w, _ = frame.shape
        cx, cy = w//2, h//2
        start_x = cx - gap
        start_y = cy - gap

        # Draw grid
        for r in range(3):
            for c in range(3):
                x = start_x + c*gap
                y = start_y + r*gap
                cv2.rectangle(frame, (x-15, y-15), (x+15, y+15), (0,255,0), 2)

        cv2.putText(frame, f"{window_name} Face - Press C to capture",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.imshow("Scan Cube", frame)

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

            final = correct_face(face_colors)
            return final

        if k == ord('q'):
            print("Quit pressed.")
            exit()


# MAIN FLOW ==================

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error")
    exit()

faces_order = [
    ("Front", "F"),
    ("Right", "R"),
    ("Back", "B"),
    ("Left", "L"),
    ("Up", "U"),
    ("Down", "D")
]

all_faces = {}

for face_name, face_key in faces_order:
    all_faces[face_key] = scan_one_face(face_name, cap)
    print(f"\n✔ Saved {face_name} face:", all_faces[face_key])

# Save to JSON
with open("cube_faces.json", "w") as f:
    json.dump(all_faces, f, indent=4)

print("\n🎉 All faces scanned successfully!")
print("Saved to cube_faces.json")

cap.release()
cv2.destroyAllWindows()
