import cv2
import os

# Create captures folder if not exists
if not os.path.exists("captures"):
    os.makedirs("captures")

cap = cv2.VideoCapture(0)

print("\nPress keys to capture faces:")
print("F = Front")
print("R = Right")
print("L = Left")
print("B = Back")
print("U = Up")
print("D = Down")
print("Q = Quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imshow("Capture Cube Faces", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('f'):
        cv2.imwrite('captures/front.jpg', frame)
        print("Front face captured!")

    elif key == ord('r'):
        cv2.imwrite('captures/right.jpg', frame)
        print("Right face captured!")

    elif key == ord('l'):
        cv2.imwrite('captures/left.jpg', frame)
        print("Left face captured!")

    elif key == ord('b'):
        cv2.imwrite('captures/back.jpg', frame)
        print("Back face captured!")

    elif key == ord('u'):
        cv2.imwrite('captures/up.jpg', frame)
        print("Up face captured!")

    elif key == ord('d'):
        cv2.imwrite('captures/down.jpg', frame)
        print("Down face captured!")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
