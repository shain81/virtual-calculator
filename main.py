import cv2
from cvzone.HandTrackingModule import HandDetector
import time


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y, img):  # اصلاح ورودی img
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
            return True
        return False


# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1920)  # width
cap.set(4, 1080)  # height
detector = HandDetector(detectionCon=0.8, maxHands=1)

if not cap.isOpened():
    print("webcam is not opened")
    exit()

# creating buttons
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

buttonList = [Button((x * 100 + 800, y * 100 + 150), 100, 100, buttonListValues[y][x]) for x in range(4) for y in
              range(4)]

# variables
myEquation = ''
delaycounter = 0

# loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # draw all buttons
    cv2.rectangle(img, (800, 50), (1200, 150), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800, 50), (1200, 150), (50, 50, 50), 3)

    for button in buttonList:
        button.draw(img)

    # check for hand
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

        x, y, _ = lmList[8]  # اصلاح مقدار x, y

        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y, img) and delaycounter == 0:
                    myValue = buttonListValues[i % 4][i // 4]  # اصلاح مقدار
                    if myValue == "=":
                        try:
                            myEquation = str(eval(myEquation))  # اصلاح محاسبه
                        except:
                            myEquation = "Error"
                    else:
                        myEquation += myValue
                    delaycounter = 1

    # avoid duplicates
    if delaycounter != 0:
        delaycounter += 1
        if delaycounter > 10:
            delaycounter = 0

    # display the equation/result
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    # display image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEquation = ''

    if key == ord('q'):  # اضافه کردن کلید خروج
        break
cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cap.release()
cv2.destroyAllWindows()
