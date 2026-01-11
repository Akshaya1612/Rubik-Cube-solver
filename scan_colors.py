import cv2

# Define color ranges for cube stickers
COLOR_RANGES = {
    "white": ([0, 0, 200], [180, 30, 255]),
    "yellow": ([20, 100, 100], [30, 255, 255]),
    "red": ([0, 100, 100], [10, 255, 255]),
    "orange": ([10, 100, 100], [20, 255, 255]),
    "green": ([40, 50, 50], [90, 255, 255]),
    "blue": ([90, 50, 50], [130, 255, 255])
}

def detect_color(hsv_val):
    for color, (lower, upper) in COLOR_RANGES.items():
        lower = tuple(lower)
        upper = tuple(upper)
        if all(lower[i] <= hsv_val[i] <= upper[i] for i in range(3)):
            return color
    return "unknown"


cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Draw a square in the center for user to place one sticker
    h, w, _ = frame.shape
    size = 100
    x1, y1 = w // 2 - size, h // 2 - size
    x2, y2 = w // 2 + size, h // 2 + size

    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    cv2.imshow("Scan Cube Color", frame)

    key = cv2.waitKey(1)

    if key == ord('c'):  # capture color
        center_pixel = frame[h // 2, w // 2]
        hsv_pixel = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[h // 2, w // 2]

        detected = detect_color(hsv_pixel)
        print("Detected Color:", detected)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
