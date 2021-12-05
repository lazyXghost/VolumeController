import cv2
import time
import HandTrackingModule as htm
from subprocess import call

red = (0, 0, 255)
blue = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)
redBlue = (255, 0, 255)


def showFrameRate(img,pTime):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    cv2.putText(img, "FPS: "+str(int(fps)), (40, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)  # displaying fps on top of img
    return img,cTime


def showVolume(img, vol):
    cv2.rectangle(img, (48, 147), (73, 403), (0, 0, 0), 3)
    
    volColor = green
    if(vol<30):
        volColor = blue
    elif(vol>70):
        volColor = red

    cv2.rectangle(img, (50, int(400 - (vol / 100) * 250)), (70, 400), volColor, cv2.FILLED)
    cv2.putText(img, str(int(vol)), (40, 140), cv2.FONT_HERSHEY_COMPLEX, 1, black, 3)
    return img

# function to show the volume line in between thumb and index finger and returning its length
def showLine(img, lmList, vol):
    thumbTip = (lmList[4][1],lmList[4][2])
    indexTip = (lmList[8][1],lmList[8][2])
    center = (int((thumbTip[0]+indexTip[0])/2), int((thumbTip[1]+indexTip[1])/2))

    circles = [thumbTip, indexTip]
    for i in circles:
        cv2.circle(img, i, 15, redBlue, cv2.FILLED)
    
    centerColor = green
    lineColor = green
    if vol > 70:
        centerColor = red
        lineColor = red
    elif vol < 30:
        centerColor = blue
        lineColor = blue

    cv2.circle(img, center, 15, centerColor, cv2.FILLED)
    cv2.line(img, thumbTip, indexTip, lineColor, 3)

    length = (((indexTip[1] - thumbTip[1]) ** 2) + ((indexTip[0] - thumbTip[0]) ** 2)) ** 0.5
    ratio = (((lmList[1][1]-lmList[2][1])**2)+((lmList[1][2]-lmList[2][2])**2))**0.5
    return img,length,ratio

# function to change the volume of the computer
def volChange(nwvol, lsvol, vol, ratio, snstvty):
    if abs(nwvol - lsvol) > snstvty:
        if nwvol < (3*ratio)/8:
            vol = 0
        elif nwvol > (30*ratio)/8:
            vol = 100
        else:
            vol = ((30*nwvol) / ratio) - 10
        call(["amixer", "-D", "pulse", "sset", "Master", str(int(vol)) + "%"])
    return nwvol,vol


cap = cv2.VideoCapture(0)  # getting videocapture
wcam, hcam = 1280, 1080  # set the height and width of display window
cap.set(3, wcam)
cap.set(4, hcam)

# declaring variables
pTime = 0
lsvol = 0
i = 0
vol = 0
sensitivity = 10  # decrease this value to make it more sensitive
volColor = blue   # define variable volcolor with initial color blue
lineColor = blue  # define variable linecolor with initial color blue
noOfHands = 1     # no of hands to be detected by program, change it to 2 if you want to check for two hands

# defining class object for hand detection,increase detection confidence so that it dont detect false hands
detector = htm.handDetector(maxHands=noOfHands, detectionCon=0.8)

while True:
    success, img = cap.read()
    img, lmList = detector.Hands(img, drawDots=False) # drawing hands skeleton on img and getting coordinates in lmList

    img = showVolume(img, vol)  # showing volume bar on left
    img, pTime = showFrameRate(img, pTime) # calling function to put fps on top of image

    if len(lmList) != 0:
        img,nwvol,ratio = showLine(img, lmList, vol)
        lsvol,vol = volChange(nwvol,lsvol,vol,ratio,sensitivity)

    cv2.imshow("Image", img)  # displaying img with hand skeleton on top of it
    cv2.waitKey(1)
