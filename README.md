# Interactive AprilTag Detection Script

Detect AprilTags in images using multiple tag families with a user-friendly, interactive CLI.

---

## Features

- Interactive prompt to select AprilTag families for scanning
- Supports all major AprilTag families via `pupil-apriltags`
- Shows number of tags detected, their family, and IDs
- Visualizes detection results with OpenCV and Matplotlib

---

## Installation

Python >= 3.8 required.  
Install dependencies:

```bash
pip install pupil-apriltags opencv-python matplotlib numpy
```

## Usage
Run the script

```bash
python src/apriltag_interactive.py
```
- Enter the path to your image when prompted
- Select which tag families to scan (by number, “all”, or Enter for default)
- View detection summary and visualization

## Output
- Lists total tags found, families, and tag IDs
- Visualizes tags with bounding boxes and IDs
