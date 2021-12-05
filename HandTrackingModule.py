# ID for the points of the hands are-:
# WRIST ----> TOP
# 0,1,2,3,4 - thumb
# 5,6,7,8 - index finger
# 9,10,11,12 - middle finger
# 13,14,15,16 - third finger
# 17,18,19,20 - pinky finger

import cv2
import mediapipe as mp


class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # declaring variables to use in the function while detecting hand
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands, detectionCon, trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.imgRGB = None
        self.landmarks = None

    def Hands(self, img, handNo=0, drawHand=True, drawDots=True, dotSize=5):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converting screenshot of video capture to RGB as openCV can detect RGB image more efficiently
        self.landmarks = self.hands.process(self.imgRGB).multi_hand_landmarks  # storing hand landmarks in self.landmarks

        lmList = []
        if self.landmarks:  # getting inside if we can find hand landmarks i.e. hand is visible on camera
            for handLms in self.landmarks:  # drawing points and lines on hands
                if drawHand:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

            myHand = self.landmarks[handNo]  # getting landmarks coordinates in lmList
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # lm gives position in terms of x,y like 0.3,0.4
                lmList.append([id, cx, cy])  # cx, cy gives position in terms of number or a point
                if drawDots: # to draw a circles on top
                    # if id==4:  # If we want to draw only on the top of thumb(4 is index of thumb)
                    cv2.circle(img, (cx, cy), dotSize, (255, 0, 255), cv2.FILLED)

        return img, lmList
