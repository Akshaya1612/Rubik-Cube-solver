import cv2
import numpy as np

# Define BGR color ranges for Rubik's cube
COLOR_RANGES = {
    "white": ([200, 200, 200], [255, 255, 255]),
    "yellow": ([0, 200, 200], [50, 255, 255]),
    "red": ([0, 0, 150], [80, 80, 255]),
    "orange": ([0, 100, 200], [80, 180, 255]),
    "blue": ([150, 0, 0], [255, 80, 80]),
    "green": ([0, 150, 0], [80, 255, 80])
}

def detect_color(bgr_pixel):
    for color, (lower, upper) in COLOR_RANGES.items():
        lower = np.array(lower)
        upper = np.array(upper)
        if cv2.inRange(np.array([[bgr_pixel]]), lower, upper) == 255:
            return color
    return "unknown"


def extract_face_colors(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, "Image not found"

    h, w, _ = img.shape

    # Divide into 3x3 grid
    step_h = h // 3
    step_w = w // 3

    colors = []

    for row in range(3):
        for col in range(3):
            y = row * step_h + step_h // 2
            x = col * step_w + step_w // 2
            pixel = img[y, x]

            color = detect_color(pixel)
            colors.append(color)

    return colors, None
