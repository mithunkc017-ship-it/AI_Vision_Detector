# AI Vision Detector

AI Vision Detector is a real-time object detection application that combines a local YOLO model with Google Gemini Vision. It opens a laptop or USB camera, detects objects using Ultralytics YOLO11, overlays labels and bounding boxes, and sends camera frames to Gemini every five seconds for an easy-to-read identification.

The application also displays the number of detected objects and an estimated frames-per-second value in an on-screen dashboard.

## Features

- Real-time camera capture through OpenCV
- YOLO11 object detection with confidence filtering
- Bounding boxes and object labels drawn directly onto the video frame
- Gemini Vision identification of the main physical item in the camera view
- Automatic Gemini analysis every five seconds
- Live object count and FPS display
- Multi-threaded Gemini requests so image recognition does not block the video preview
- Lightweight camera and Gemini API test scripts

## How It Works

1. The application loads the local `yolo11n.pt` YOLO model.
2. OpenCV captures frames from the default webcam.
3. YOLO processes each frame and identifies visible objects.
4. OpenCV draws the detection results and dashboard text onto the frame.
5. Every five seconds, a separate thread sends a copy of the current frame to the Gemini Vision API.
6. Gemini returns a short common name for the main item, which is displayed on the camera feed.

Gemini processing runs asynchronously, but YOLO detection and the main camera loop continue while a request is in progress.

## Technologies Used

| Technology | Purpose |
| --- | --- |
| Python | Main application language |
| OpenCV | Camera access and video rendering |
| Ultralytics YOLO11 | Real-time local object detection |
| Google Gemini API | Vision-based item identification |
| Google Gen AI SDK | Gemini API integration |
| Pillow | Conversion of camera frames for Gemini |
| python-dotenv | Loading environment variables from `.env` |

## Requirements

- Windows 10 or 11
- Python 3.10 or newer
- A webcam or USB camera
- Internet access for Gemini API requests
- A Google Gemini API key

## Project Structure

```text
AI-Vision-Detector/
|-- app.py           # Main detection and Gemini Vision application
|-- camera_test.py   # Tests available webcams and frame capture
|-- gemini_test.py   # Verifies the Gemini API key and connection
|-- yolo11n.pt       # Pre-trained YOLO11 Nano model
|-- .env             # Local API key configuration
|-- .gitignore       # Excluded environment and cache files
`-- README.md        # Project documentation
```

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/mithunkc017-ship-it/AI_Vision_Detector.git
cd AI_Vision_Detector
```

### 2. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents script execution, allow it for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install opencv-python pillow python-dotenv google-genai ultralytics
```

### 4. Configure the Gemini API key

Create a file named `.env` in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with an API key from Google AI Studio. Never commit your real API key or share it publicly.

## Usage

### Run the complete application

```powershell
python app.py
```

The video window is named **AI Vision Detector**. It displays:

- detected objects and confidence-based bounding boxes
- total object count
- approximate FPS
- the latest or in-progress Gemini identification

Press `Q` while the video window is active to close the application.

### Test the camera

```powershell
python camera_test.py
```

This script checks camera indexes `0`, `1`, and `2` and opens the first working camera. Press `Q` to stop the preview.

### Test the Gemini connection

```powershell
python gemini_test.py
```

A successful configuration prints a Gemini response. This test does not send an image.

## Detection Settings

The main settings are currently defined in `app.py`:

| Setting | Current value | Description |
| --- | ---: | --- |
| Camera width | 1280 px | Requested OpenCV frame width |
| Camera height | 720 px | Requested OpenCV frame height |
| Detection confidence | 0.15 | Minimum YOLO confidence threshold |
| YOLO image size | 640 px | Input size used for YOLO inference |
| Gemini interval | 5 seconds | Delay between automatic image requests |
| Gemini model | `gemini-flash-latest` | Vision model used for item identification |

## Troubleshooting

### Camera not found

- Make sure another application is not exclusively using the webcam.
- Check Windows camera privacy settings.
- Test the camera with `python camera_test.py`.
- If the default webcam is not index `0`, update the camera index in `app.py`.

### Gemini API key not found

Confirm that `.env` exists in the project root and contains:

```text
GEMINI_API_KEY=your_api_key_here
```

Restart the application after changing the environment file.

### YOLO model not found

Run the application from the project root. The application loads `yolo11n.pt` using a relative path.

### Low FPS

- Close other camera or GPU-intensive applications.
- Lower the capture resolution or YOLO `imgsz` value.
- Use a webcam with a lower or more stable resolution.
- A CPU-only system may run at a lower FPS than a GPU-enabled system.

### Slow or failed Gemini requests

- Check your internet connection.
- Verify that the API key is valid and has available quota.
- Gemini requests repeat only after an existing request finishes or fails.

## Privacy and API Usage

This project sends full-resolution camera frame copies to Google Gemini at regular intervals. Use it only in appropriate environments and inform anyone who may be visible to the camera. API availability, quota limits, and data-handling policies are controlled by the user's Gemini account and Google's current terms.

## Future Improvements

- User-configurable camera and detection settings
- Support for selecting the camera and YOLO model
- Manual Gemini analysis shortcut
- Pause and resume Gemini auto-analysis
- Detection confidence indicators
- Multi-language Gemini responses
- GPU/CUDA setup detection
- Image and video export controls
- REST or desktop UI interface

## License

Add a license file if you plan to distribute or publish this project. Until a license is included, the repository's usage rights remain with the project owner.
