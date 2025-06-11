# Interactive AprilTag Detection Script

import cv2
import numpy as np
from pupil_apriltags import Detector
import matplotlib.pyplot as plt
import os

# Available AprilTag families
available_families = [
    'tag16h5', 'tag25h9', 'tag36h11', 
    'tagCircle21h7', 'tagCircle49h12', 'tagCustom48h12', 
    'tagStandard41h12', 'tagStandard52h13'
]

print("="*60)
print("APRILTAG DETECTION SCRIPT")
print("="*60)

# Get image path from user
while True:
    image_path = input("Enter path to your image: ").strip()
    if os.path.exists(image_path):
        break
    else:
        print("❌ File not found. Please enter a valid image path.")

# Show available families
print(f"\nAvailable AprilTag families:")
for i, family in enumerate(available_families, 1):
    print(f"{i:2d}. {family}")

print(f"\nOptions:")
print(f"- Enter numbers separated by commas (e.g., 1,2,4)")
print(f"- Enter 'all' to scan all families")
print(f"- Press Enter for common families (tag36h11, tag25h9, tag16h5)")

# Get family selection from user
while True:
    selection = input("Select families: ").strip()
    
    if selection == "":
        # Default to common families
        selected_families = ['tag36h11', 'tag25h9', 'tag16h5']
        print("Using default families: tag36h11, tag25h9, tag16h5")
        break
    elif selection.lower() == "all":
        selected_families = available_families.copy()
        print("Using all available families")
        break
    else:
        try:
            # Parse number selection
            numbers = [int(x.strip()) for x in selection.split(',')]
            if all(1 <= num <= len(available_families) for num in numbers):
                selected_families = [available_families[num-1] for num in numbers]
                print(f"Selected families: {', '.join(selected_families)}")
                break
            else:
                print(f"❌ Please enter numbers between 1 and {len(available_families)}")
        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by commas, 'all', or press Enter for defaults.")

print(f"\nProcessing image: {image_path}")
print(f"Scanning {len(selected_families)} families...")
print("="*60)

# Load and prepare image
try:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
except Exception as e:
    print(f"❌ Error loading image: {e}")
    exit(1)

# Scan for tags across selected families
all_detections = []
detected_families = []
tag_values = []

print("Scanning for AprilTags...")

for family in selected_families:
    try:
        detector = Detector(families=family)
        detections = detector.detect(gray)
        
        if detections:
            detected_families.append(family)
            all_detections.extend(detections)
            for det in detections:
                tag_values.append(det.tag_id)
            print(f"✓ Found {len(detections)} tags in {family}")
        else:
            print(f"  No tags found in {family}")
            
    except Exception as e:
        print(f"❌ Error with {family}: {e}")

# INFO - 3 lines
print("\n" + "="*50)
print("INFO:")
print(f"Total AprilTags detected: {len(all_detections)}")
print(f"Families with detections: {len(detected_families)}")
print(f"Tag IDs found: {sorted(set(tag_values))}")
print("="*50)

# Required results
apriltags_count = len(all_detections)
families_detected = detected_families
apriltag_values = tag_values

print(f"\nHow many apriltags read: {apriltags_count}")
print(f"Which families detected: {families_detected}")
print(f"Value of apriltags: {apriltag_values}")

# Print detailed detection info first
if all_detections:
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
    color_names = ["Red", "Green", "Blue", "Yellow", "Magenta"]
    
    print(f"\nDetailed Results:")
    for i, det in enumerate(all_detections):
        color_name = color_names[i % len(color_names)]
        print(f"Tag {i+1} ({color_name}): ID={det.tag_id}, Center=({det.center[0]:.1f}, {det.center[1]:.1f}), Confidence={det.decision_margin:.2f}")

# Visualize results
if all_detections:
    result_image = image.copy()
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
    
    for i, detection in enumerate(all_detections):
        color = colors[i % len(colors)]
        
        # Draw tag outline
        corners = detection.corners.astype(int)
        cv2.polylines(result_image, [corners], True, color, 2)
        
        # Draw center and tag number (bigger, bolder font)
        center = tuple(detection.center.astype(int))
        cv2.circle(result_image, center, 5, color, -1)
        cv2.putText(result_image, f"ID:{detection.tag_id}", 
                   (center[0]+10, center[1]-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3) 
    
    print(f"\nDisplaying image with detected tags...")
    
    # Show result
    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
    plt.title(f"AprilTag Detection - {apriltags_count} tags found")
    plt.axis('off')
    plt.show()
else:
    print("\n❌ No AprilTags detected in the image")
    print("Try:")
    print("- Using a different image")
    print("- Selecting more families")
    print("- Checking image quality and lighting")

print(f"\nScript completed!")
