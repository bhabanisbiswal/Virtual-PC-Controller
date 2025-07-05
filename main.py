import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

# Parameters
wCam, hCam = 640, 480  # Webcam resolution
frameR = 100  # Frame reduction for smoother mouse movement
smoothening = 7  # Smoothening factor

# Initialize variables
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Capture webcam
cap = cv2.VideoCapture(0)  # Use `0` for default webcam
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize hand detector
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()  # Get screen resolution

# Resize factor for the output window
output_width = 1280  # Larger display width
output_height = 720  # Larger display height

while True:
    # 1. Find hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Check if landmarks are detected
    if len(lmList) != 0:
        # Get the tip of the index and middle fingers
        x1, y1 = lmList[8][1:]  # Index finger
        x2, y2 = lmList[12][1:]  # Middle finger

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)

        # 4. Only Index Finger: Moving Mode
        if len(fingers) > 2 and fingers[1] == 1 and fingers[2] == 0:
            # Convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # Smoothen the values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Move the mouse
            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 5. Both Index and Middle Fingers Up: Clicking Mode
        if len(fingers) > 2 and fingers[1] == 1 and fingers[2] == 1:
            # Find the distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # Perform mouse click if the fingers are close
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

    # 6. Display Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    # Resize image for a larger display window
    img_resized = cv2.resize(img, (output_width, output_height))

    # 7. Display Image
    cv2.imshow("Image", img_resized)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
