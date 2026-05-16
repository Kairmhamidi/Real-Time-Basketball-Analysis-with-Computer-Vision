# AI Basketball Analysis System

An AI-powered basketball analysis project built using Python, OpenCV, and YOLOv8 for detecting and tracking basketball players and the ball from video footage.

---

## Features

- Player detection and tracking
- Basketball detection and tracking
- Real-time video processing
- Video input and output support
- Custom drawing utilities
- Object trajectory visualization
- Stub-based tracking optimization

---

## Technologies Used

- Python
- OpenCV
- YOLOv8
- NumPy
- Computer Vision

---

## Project Structure

```bash
Basketball-Analysis/
│
├── drawers/
├── tracker/
├── utills/
├── models/
├── input/
├── stubes/
├── Generator/
├── main.py
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/basketball-analysis-system.git
```

Move into the project folder:

```bash
cd basketball-analysis-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the project:

```bash
python main.py
```

Output videos will be saved in:

```bash
Generator/
```

---

## Notes

Large files such as:
- datasets
- videos
- trained models
- pickle stub files

are excluded from the repository using `.gitignore`.

---

## Future Improvements

- Team classification
- Player statistics
- Speed estimation
- Court detection
- Shot detection
- Real-time webcam support

---

## Author

Karim Hamidi
