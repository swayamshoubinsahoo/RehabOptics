# RehabOptics

Markerless Real-Time Kinematic Tracking & Biomechanical Assessment Engine

## Architecture Overview
RehabOptics is an edge-based monocular computer vision application designed to calculate lower-limb joint planar kinematics in real time. The system executes continuous angular vector mathematics to provide instantaneous range-of-motion (ROM) biofeedback, log repetition segmentations, and synthesize automated clinical mobility evaluations without requiring external sensor hardware.

- **Computer Vision Pipeline**: High-throughput edge motion segmentation and skeletal joint node tracking operating at 70+ FPS.
- **Kinematic Analysis**: Dynamic vector trigonometry across hip-knee-ankle kinetic chains with automated rep phase detection.
- **Automated Clinical Synthesis**: High-dimensional diagnostic evaluation parsing excursion depth, extension symmetry, and mechanical deficits.

## Getting Started
```powershell
# Clone repository
git clone [https://github.com/swayamshoubinsahoo/RehabOptics.git](https://github.com/swayamshoubinsahoo/RehabOptics.git)
cd RehabOptics

# Install dependencies
py -m pip install opencv-python numpy google-genai

# Configure environment and run
$env:GEMINI_API_KEY = "your_api_key_here"
py main.py