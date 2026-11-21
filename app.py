
import os
import cv2
import time
import threading
from PIL import Image
from dotenv import load_dotenv
from google import genai
from ultralytics import YOLO

# Load Gemini API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open laptop camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not camera.isOpened():
    raise RuntimeError("Camera not found!")

gemini_result = "Press G to identify an item"
gemini_busy = False
previous_time = time.time()

# Automatic Gemini recognition settings
AUTO_INTERVAL = 5  # seconds
last_gemini_request = time.monotonic()
auto_detection = True


# Identify object using Gemini Vision
def identify_item(frame):
    global gemini_result, gemini_busy

    try:
        # Convert OpenCV BGR image to RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_image)

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[
                "Identify the main physical item shown in "
                "this image. Return its common name in "
                "at most 6 words. If unclear, say Unknown.",
                image
            ]
        )

        gemini_result = (
            response.text.strip()
            if response.text
            else "Unknown item"
        )

        print("Gemini identified:", gemini_result)

    except Exception as error:
        gemini_result = "Gemini request failed"
        print("Gemini Error:", error)

    finally:
        gemini_busy = False


print("AI Vision Detector Started!")
print("Press G to identify an item")
print("Press Q to quit")

while True:
    success, frame = camera.read()

    if not success:
        print("Camera frame error!")
        break

    # YOLO real-time detection
    results = model.predict(
        source=frame,
        conf=0.15,
        imgsz=640,
        verbose=False
    )

    annotated_frame = results[0].plot()

    
    # Automatic Gemini Vision recognition
    current_auto_time = time.monotonic()

    if (
        auto_detection
        and not gemini_busy
        and current_auto_time - last_gemini_request >= AUTO_INTERVAL
    ):
        gemini_busy = True
        last_gemini_request = current_auto_time

        threading.Thread(
            target=identify_item,
            args=(frame.copy(),),
            daemon=True
        ).start()


    object_count = len(results[0].boxes)

    # Calculate FPS
    current_time = time.time()
    fps = 1 / max(current_time - previous_time, 0.001)
    previous_time = current_time

    # Dashboard background
    cv2.rectangle(
        annotated_frame,
        (0, 0),
        (650, 125),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        annotated_frame,
        "AI VISION DETECTOR",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Objects: {object_count} | FPS: {fps:.1f}",
        (15, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # Gemini result
    display_text = (
        "Gemini: Identifying..."
        if gemini_busy
        else f"Gemini: {gemini_result}"
    )

    cv2.putText(
        annotated_frame,
        display_text[:65],
        (15, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.imshow("AI Vision Detector", annotated_frame)

    key = cv2.waitKey(1) & 0xFF

    print("Automatic Gemini recognition enabled!")
    print("Gemini analyzes the camera every 5 seconds.")

    # Press Q to quit
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
