# 🏋️‍♂️ AI Fitness Form Analyzer & Rep Counter

This project is an AI-powered **exercise rep counter and form analyzer** built using [MediaPipe](https://google.github.io/mediapipe/) and OpenCV. It tracks body landmarks to automatically count repetitions and provide feedback on posture/form for various exercises in real time via webcam.

## 🚀 Features

- Real-time pose detection using MediaPipe
- Automated rep counting for:
  - Bicep Curls
  - Squats
  - Pushups
  - Crunches
  - Overhead Triceps Extension
  - Deadlifts
  - Lateral Raises
  - Barbell Rows
  - Lunges
- Form analysis and feedback using joint angles
- Visual warnings for poor posture (e.g., bent back, shallow squats)
- Modular structure with one file per exercise

## 🧠 How It Works

Each exercise uses body landmarks (hip, knee, ankle, etc.) to calculate joint angles and determine movement stages (`up`, `down`). Once a rep cycle is complete, it increments the counter. Feedback is given when posture or depth falls outside safe thresholds.

## 🧱 Project Structure
```
MyTrainer/
│
├── app/
│   └── models/
│       ├── biceps_curl_counter.py
│       ├── squats_counter.py
│       ├── pushup_counter.py
│       ├── crunch_counter.py
│       ├── overhead_triceps_counter.py
│       ├── deadlift_counter.py
│       ├── lateral_raise_counter.py
│       ├── barbell_row_counter.py
│       └── lunges_counter.py
│
├── common.py              # Shared utilities: angle calculation, drawing helpers
├── pose_tracker.py        # Landmark tracker class
├── main.py                # Main CLI to choose exercise
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

```


---

## 🖥️ How to Run

### 1. Clone the Repository

```
git clone https://github.com/your-username/ai-fitness-analyzer.git
cd ai-fitness-analyzer
```

### 2. Set Up Environment
```
pip install -r requirements.txt
```

### 3. Run the Program
```
python main.py
```


Follow the on-screen prompts to select an exercise from 1 to 9.

---

## 📦 Dependencies

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy

Install all using:
```
pip install -r requirements.txt
```

---

## 🛠️ Future Plans

- 3D Pose Estimation for more accurate form correction
- Voice assistant feedback
- Mobile app integration (React Native)
- Object detection for weights/machines
- Workout history tracker

---

## 👤 Author

Built by [Sanish Shrestha](https://github.com/SanishCodes)  
Inspired by the vision to bring AI into personal fitness.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).


