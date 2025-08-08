import cv2
from time import time
import numpy as np
import cvzone
from pynput.keyboard import Controller
from HandTrackingModule import handDetector  # Your custom hand tracking module

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize hand detector
detector = handDetector(detectionCon=0.8)

# Keyboard layout
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText = ""
keyboard = Controller()


class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


# Create button list
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Hover and click tracking
hoverStartTime = None
hoveredButton = None
clickedButtons = {}  # Stores recently clicked buttons with timestamp


# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img, draw=True)
    lmList, bboxInfo = detector.findPosition(img)

    # Draw all buttons
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        # Show clicked button in green for 0.5s
        if button.text in clickedButtons:
            if time() - clickedButtons[button.text] < 0.5:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
            else:
                del clickedButtons[button.text]
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)

        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    if lmList:
        index_x, index_y = lmList[8][1], lmList[8][2]
        hovering = False

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Check if finger is over this button
            if x < index_x < x + w and y < index_y < y + h:
                hovering = True

                if hoveredButton != button.text:
                    hoveredButton = button.text
                    hoverStartTime = time()
                else:
                    duration = time() - hoverStartTime
                    cv2.putText(img, f"{int(duration)}s", (x + 20, y - 10),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                    if duration >= 2:
                        keyboard.press(button.text)
                        keyboard.release(button.text)
                        finalText += button.text
                        print(f"Pressed: {button.text}")
                        clickedButtons[button.text] = time()
                        hoveredButton = None
                        hoverStartTime = None
                break

        if not hovering:
            hoveredButton = None
            hoverStartTime = None

    # Draw typed text area
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
