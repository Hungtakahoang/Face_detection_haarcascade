from serialModule import SerialTransfer 
from time import sleep
import cv2

arduino = SerialTransfer("COM5")
imageON = cv2.imread("../img/light_bulb.png")
imageOFF = cv2.imread("../img/light_bulb_off.png")
percent_scale = 0.6
height = int(imageON.shape[0]*percent_scale)
width = int(imageON.shape[1]*percent_scale)
dim = (width, height)
imageON = cv2.resize(imageON, dim)
imageOFF = cv2.resize(imageOFF, dim)

while True:
    arduino.sendData([1])
    sleep(3)
    arduino.sendData([0])
    sleep(1)
