import cv2
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
from HandTrackingModule import handDetector  # Import your custom module

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)  # Set height

# Initialize HandDetector
detector = handDetector(detectionCon=0.8)

# Define keyboard keys layout
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText = ""
keyboard = Controller()
keyPressed = False  # Flag to prevent duplicate key presses
lastKey = None  # Track the last pressed key


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


def drawAll(img, buttonList):
    """Draw all buttons on the screen."""
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    # Detect hands
    img = detector.findHands(img, draw=True)
    lmList, bboxInfo = detector.findPosition(img)

    # Draw keyboard
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Check if index finger is over a button
            if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                # Check distance between index and middle finger
                l, _, _ = detector.findDistance(8, 12, img, draw=False)

                if l < 30 and (not keyPressed or lastKey != button.text):
                    keyboard.press(button.text)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    keyPressed = True
                    lastKey = button.text  # Store last pressed key
                    sleep(0.15)

        # Reset key press flag when finger moves away from keys
        if all(not (x < lmList[8][1] < x + w and y < lmList[8][2] < y + h) for button in buttonList):
            keyPressed = False
            lastKey = None  # Reset last key

    # Display the typed text
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Show image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
