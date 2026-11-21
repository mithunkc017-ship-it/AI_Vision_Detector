
import cv2

for camera_index in [0, 1, 2]:
    print(f"Testing camera {camera_index}...")

    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Camera not available")
        cap.release()
        continue

    ret, frame = cap.read()

    if ret:
        print(f"Camera {camera_index} working!")
        cv2.imshow("Camera Test - Press Q to quit", frame)

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Frame capture failed")
                break

            cv2.imshow("Camera Test - Press Q to quit", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        break

    print("Could not capture frame")
    cap.release()

cv2.destroyAllWindows()
