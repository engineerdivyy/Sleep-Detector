# Sleep Detector for Drivers

A real-time computer vision application that detects driver drowsiness using facial landmarks and eye aspect ratio analysis. When drowsiness is detected, the system triggers an audio alarm to alert the driver.

## Features

- Real-time eye detection using webcam
- Drowsiness detection based on eye aspect ratio (EAR)
- Audio alarm when driver shows signs of drowsiness
- Visual indicators (color-coded eye rectangles)
- Adjustable sensitivity thresholds

## Prerequisites

Before running this project, ensure you have:

- **Python 3.7+** installed on your system
- A working webcam
- An audio file named `alarm.mp3` in the project directory

## Installation

### 1. Clone or Download the Project
```bash
cd Sleep-Detector
```

### 2. Install Required Dependencies

Run the following command to install all required Python packages:

```bash
pip install opencv-python dlib scipy imutils pygame
```

**Package Descriptions:**
- `opencv-python` - Computer vision library for video capture and image processing
- `dlib` - Machine learning library for facial landmark detection
- `scipy` - Scientific computing library (for distance calculations)
- `imutils` - OpenCV convenience functions
- `pygame` - For playing audio alarms

### 3. Download the Face Landmarks Model

Download the `shape_predictor_68_face_landmarks.dat` file from:
- [iBUG 300-W Dataset](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

**Installation steps:**
1. Download and extract the `.bz2` file
2. Place the `shape_predictor_68_face_landmarks.dat` file in your project directory
3. Update the path in `main.py` if needed (currently set to: `C:\Users\yadav\OneDrive\Desktop\day 17\shape_predictor_68_face_landmarks.dat`)

### 4. Add Your Alarm Audio File

Add an audio file named `alarm.mp3` to the project directory. This will play when drowsiness is detected.

## Configuration

You can adjust the following parameters in `main.py`:

```python
ALARM_FILE = "alarm.mp3"                      # Path to your alarm audio file
EYE_ASPECT_RATIO_THRESHOLD = 0.25             # EAR threshold (lower = more sensitive)
EYE_ASPECT_RATIO_CONSEC_FRAMES = 20           # Frames threshold before triggering alarm
```

**Adjusting Sensitivity:**
- Lower `EYE_ASPECT_RATIO_THRESHOLD` = More sensitive (detects drowsiness faster)
- Higher `EYE_ASPECT_RATIO_THRESHOLD` = Less sensitive (requires more obvious eye closure)
- `EYE_ASPECT_RATIO_CONSEC_FRAMES` = Number of consecutive frames with closed eyes before alarm triggers

## Running the Application

1. Open a terminal/command prompt in the project directory
2. Run the application:

```bash
python main.py
```

3. The webcam feed will open in a new window showing:
   - **Green rectangles** around eyes = Eyes are open (normal)
   - **Red rectangles** around eyes = Drowsiness detected (alarm will sound)

4. To exit the application, press **Q** on your keyboard

## How It Works

1. **Face Detection** - Uses dlib's frontal face detector to locate faces in the video stream
2. **Facial Landmarks** - Detects 68 facial landmarks including eye coordinates
3. **Eye Aspect Ratio (EAR)** - Calculates the ratio of vertical to horizontal eye distances
4. **Drowsiness Detection** - If EAR falls below the threshold for consecutive frames, drowsiness is detected
5. **Alarm Trigger** - An audio alarm plays and a visual alert appears on screen

## Troubleshooting

### Common Issues

**Issue: "shape_predictor_68_face_landmarks.dat not found"**
- Solution: Download the file and update the path in `main.py` line 26

**Issue: "No module named 'dlib'"**
- Solution: Install dlib using `pip install dlib` (may take a few minutes to compile)

**Issue: Alarm doesn't play**
- Solution: Ensure `alarm.mp3` exists in the project directory and pygame is properly installed

**Issue: Webcam not detected**
- Solution: Check if another application is using your webcam or try changing the camera index from `0` to `1` in `main.py` line 34

**Issue: Low FPS or laggy detection**
- Solution: The video is resized to 960x720. You can reduce this for better performance or increase for better quality

## Project Structure

```
Sleep-Detector/
├── main.py                                    # Main application file
├── README.md                                  # This file
├── alarm.mp3                                  # Your alarm audio file
└── shape_predictor_68_face_landmarks.dat      # Face landmarks model
```

## License

This project is open source and available under the MIT License.

## Author

Created as a driver safety application to prevent accidents caused by driver drowsiness.
