import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

wCam, hCam = 640, 480
frameR = 100#reduced boundary for pointer movement
smoothening = 7

pTime = 0 #fps previous time
plocX, plocY = 0, 0#previous cursor/pointer loc
clocX, clocY = 0, 0#current curser/pointer loc

cap = cv2.VideoCapture(0)
cap.set(3, wCam)#set width
cap.set(4, hCam)#set height

detector = htm.handDetector(maxHands=1)#for one hand
wScr, hScr = pyautogui.size()#Get screen size

output_width = 640
output_height = 480#output display

while True:
    success, img = cap.read()#take from cap(camera input)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)#landmark for hand

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]#index finger tip
        x2, y2 = lmList[12][1:]#middle finger tip

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)#if hand there then draw a rectangle

        if len(fingers) > 2 and fingers[1] == 1 and fingers[2] == 0:#if only index finger is there
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        if len(fingers) > 2 and fingers[1] == 1 and fingers[2] == 1:#if 2 finger are there
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 40:# 40 means distance less than 40 pixel
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

    cTime = time.time()#from 52-56 for fps calculation
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    img_resized = cv2.resize(img, (output_width, output_height))
    cv2.imshow("Hand Tracking Mouse", img_resized)#output window

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
