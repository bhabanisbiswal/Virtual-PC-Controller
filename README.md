# 🖥️ Virtual PC Controller

This project allows you to **control your PC virtually using hand gestures** via a webcam.  
It combines **computer vision** 🧠 and **gesture recognition** ✋ to create two main features:

1. ⌨ **Virtual Keyboard** – Type by hovering your finger over keys on a virtual keyboard displayed on the screen.
2. 🖱 **Virtual Mouse** – Move and click your mouse cursor using hand gestures.

---

## ✨ Features

### 🖱 Virtual Mouse

* 🎯 Move the cursor by moving your index finger within a defined region.
* 👆 Click by pinching your index and middle fingers together.
* 🔄 Smoothened cursor movement for better control.
* 🖥 Works on **any screen resolution**.

### ⌨ Virtual Keyboard

* 🖥 On-screen keyboard with QWERTY layout.
* ⏳ Hover over a key for **2 seconds** to type it.
* ✅ Visual feedback for pressed keys.
* ⚡ Real-time hand tracking with key detection.

---

## 🛠 Tech Stack

* 🐍 **Python**
* 🎥 **OpenCV** – Real-time image processing.
* 🔢 **NumPy** – Coordinate mapping & calculations.
* 🎯 **cvzone** – Easy OpenCV utilities (corner rectangles, etc.).
* ⌨ **pynput** – Simulates keyboard presses.
* 🖱 **pyautogui** – Controls mouse movements and clicks.
* ✋ **Custom Hand Tracking Module** – Built using **MediaPipe** for detecting hand landmarks.

---

## 📂 Project Structure

```
Virtual_pc_controller/
│── HandTrackingModule.py    # Custom hand tracking logic
│── main.py                  # Virtual keyboard code
│── mouse.py                 # Virtual mouse code
│── keybord.py               # Additional keyboard features
│── development.py           # Development/testing scripts
│── venv/                    # Python virtual environment
│── README.md                # Project documentation
```

---

## ⚙ How It Works

### 1️⃣ Hand Tracking

* ✋ The `HandTrackingModule` detects hand landmarks using **MediaPipe**.
* 📍 Coordinates of fingertips (index & middle fingers) are used for control.

### 2️⃣ Virtual Mouse

* 🖱 Index finger → Cursor movement.
* 👆 Index + Middle fingers together → Click action.

### 3️⃣ Virtual Keyboard

* ⏳ Finger hovering over a key for a set duration → Key press.
* 💡 Visual indication when a key is pressed.

---

## 📥 Installation

1. 📂 Clone the repository:

```bash
git clone https://github.com/bhabanibiswal/Virtual_PC_Controller.git
```

2. 📁 Navigate into the folder:

```bash
cd Virtual_pc_controller
```

3. 📦 Install dependencies:

```bash
pip install opencv-python numpy cvzone pynput pyautogui
```

4. ▶ Run the desired script:

```bash
python main.py     # Virtual Keyboard
python mouse.py    # Virtual Mouse
```

---

## 🚀 Usage

* 🎥 Ensure your webcam is connected and working.
* 💡 Maintain proper lighting for accurate hand detection.
* ✋ Use **one hand** for mouse mode and keyboard mode separately.
* ❌ Press `Q` to exit the program.

---

## 📸 Demo

![image alt](https://github.com/bhabanisbiswal/Virtual-PC-Controller/blob/d09d02cc230f955bf4f5c059ef218194fca1a57b/vlcsnap-2025-08-08-11h41m11s043.png)

![image alt](https://github.com/bhabanisbiswal/Virtual-PC-Controller/blob/68bcfe88d190f9ef89cf64c44faee2743bfdc6e1/vlcsnap-2025-08-08-11h41m30s566.png)
---

## 🔮 Future Improvements

* 🌍 Multi-language keyboard layouts.
* 🖱 More mouse gestures (drag & drop, right-click).
* 📜 Touchpad-like scrolling.
* 🎙 Integration with voice commands.

---

## 👤 Author  
**Bhabani S Biswal** – Python & AI/ML Developer  
📧 Email: [bhabanibiswalb17@gmail.com](mailto:bhabanibiswalb17@gmail.com)  
🔗 GitHub: [Bhabani S Biswal](https://github.com/bhabanisbiswal)  


---
